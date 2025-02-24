import streamlit as st
import google.generativeai as genai
import os
import docx
import fitz  
import pypandoc
import markdown
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = st.secrets["GOOGLE_API_KEY"]

# Page Configuration
st.set_page_config(page_title="AI Document Analyzer", layout="wide")

# Sidebar - Improved UI
with st.sidebar:
    st.markdown(
        """
        <style>
            .sidebar-title {
                font-size: 22px;
                font-weight: bold;
                color: #ffcc00;
                margin-bottom: 10px;
            }
            .sidebar-section {
                background-color: #1e1e2f;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
            }
            .sidebar-text {
                font-size: 16px;
                color: #cccccc;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='sidebar-title'>⚙️ Configuration</div>", unsafe_allow_html=True)
    with st.expander("Model & API Status", expanded=True):
        if api_key:
            st.success("✅ **Gemini Flash Model Active**")
        else:
            st.error("❌ API Key missing! Set it in `.env` file.")

    st.markdown("<div class='sidebar-title'>ℹ️ About</div>", unsafe_allow_html=True)
    with st.expander("Learn More", expanded=False):
        st.markdown("<div class='sidebar-text'>This tool helps analyze documents by extracting summaries and keywords. If any error or bug occurs, contact us through GitHub or email.</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-title'>📖 How to Use</div>", unsafe_allow_html=True)
    with st.expander("Steps to Use", expanded=False):
        st.markdown(
            """
            1️⃣ **Upload a document or paste text**  
            2️⃣ **Click 'Analyze'**  
            3️⃣ **View the summary & keywords**
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div class='sidebar-title'>📩 Support</div>", unsafe_allow_html=True)
    st.markdown("📧 [Contact Support](mailto:abi.developer123@gmail.com)")
    st.markdown("🌍 [View on GitHub](https://github.com/abinesh14/Document-Summarization)")

    # Recent Activity Section
    if st.session_state.get("recent_docs"):
        st.markdown("<div class='sidebar-title'>🕒 Recent Documents</div>", unsafe_allow_html=True)
        with st.expander("View Recent Files", expanded=False):
            for doc in st.session_state.recent_docs[-5:]:
                st.markdown(f"📄 **{doc}**")

# Main Content
st.markdown(
    "<h1 style='text-align: center; color: white;'>Summarization & Keyword Extraction</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Upload a document or paste text to generate a summary, detect the domain, and extract keywords.</p>",
    unsafe_allow_html=True
)

# Layout for better alignment
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 📂 Upload a Document")
    uploaded_file = st.file_uploader(
        "Upload a file", type=["txt", "doc", "docx", "pdf", "rtf", "odt", "md"], label_visibility="collapsed"
    )

with col2:
    st.markdown("### ✍️ Or Paste Your Text")
    text_input = st.text_area("Paste your text here", height=200, label_visibility="collapsed")

# Store recent documents
if "recent_docs" not in st.session_state:
    st.session_state.recent_docs = []

# Function to Extract Text from Different File Formats
def extract_text_from_file(file):
    file_extension = file.name.split(".")[-1].lower()
    try:
        if file_extension == "txt":
            return file.read().decode("utf-8")
        elif file_extension in ["doc", "docx"]:
            doc = docx.Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_extension == "pdf":
            doc = fitz.open(stream=file.read(), filetype="pdf")
            return "\n".join([page.get_text("text") for page in doc])
        elif file_extension in ["rtf", "odt", "md"]:
            return pypandoc.convert_text(file.read().decode("utf-8"), "plain", format=file_extension)
    except Exception as e:
        st.error(f"🚨 Error extracting text from file: {e}")
        return ""
    return ""

# Centered Analyze Button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
analyze_button = st.button("🔍 Analyze", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Processing Analysis
if analyze_button:
    if not api_key:
        st.error("❌ API Key not found. Please check your `.env` file.")
    else:
        genai.configure(api_key=api_key)
        document_text = ""

        if uploaded_file:
            document_text = extract_text_from_file(uploaded_file)
            st.session_state.recent_docs.append(uploaded_file.name)
        elif text_input.strip():
            document_text = text_input.strip()

        if document_text:
            try:
                prompt = f"""Analyze the following document and provide:
1. **A detailed summary** (approx. one page).
2. **The document's domain or category**.
3. **A list of domain-specific keywords**.

Format your response **EXACTLY** as:

**Summary:** [your summary here]
**Domain:** [domain here]
**Keywords:** [comma-separated keywords here]

Document Text: {document_text}"""

                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content(prompt)
                response_text = response.text

                # Extract Summary, Domain, and Keywords
                summary_start = response_text.find("**Summary:**")
                domain_start = response_text.find("**Domain:**")
                keywords_start = response_text.find("**Keywords:**")

                summary = response_text[summary_start + len("**Summary:**"):domain_start].strip()
                domain = response_text[domain_start + len("**Domain:**"):keywords_start].strip()
                keywords = response_text[keywords_start + len("**Keywords:**"):].strip()
                keywords = keywords.replace("[", "").replace("]", "").replace("'", "")

                # Display Results
                st.success("✅ Analysis Completed!")

                st.markdown("### 📌 Summary")
                st.info(summary)

                st.markdown("### 🌍 Domain")
                st.success(domain)

                st.markdown("### 🔑 Keywords")
                st.warning(keywords)

            except Exception as e:
                st.error(f"🚨 Error: {e}")
        else:
            st.warning("⚠️ Please provide some text or upload a file.")

# Recent Activity Section
if st.session_state.recent_docs:
    st.sidebar.markdown("### 🕒 Recent Documents")
    for doc in st.session_state.recent_docs[-5:]:  # Show last 5 documents
        st.sidebar.markdown(f"📄 {doc}")
