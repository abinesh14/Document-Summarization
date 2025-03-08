# AI Document Summarization

AI-powered document analyzer using Streamlit and Google's Gemini API for text summarization, domain detection, and keyword extraction.

## 🚀 Features
- 📂 **Supports multiple document formats** (TXT, DOC, DOCX, PDF, RTF, ODT, MD)
- ✍️ **Text summarization** with Gemini AI
- 🌍 **Domain detection** for uploaded content
- 🔑 **Keyword extraction** for better understanding
- 📑 **Recent documents tracking** for quick access
- 🎨 **Modern UI with enhanced sidebar features**

## 📦 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/abinesh14/Document-Summarization.git
cd Document-Summarization
```

### 2️⃣ Create a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up API Key
Create a `.env` file in the project root and add your **Google Gemini API Key**:
```env
GOOGLE_API_KEY=your_api_key_here
```

## 🎮 Usage
Run the Streamlit app using:
```bash
streamlit run app.py
```

## 📜 How It Works
1. **Upload a document** or **paste text**
2. Click **Analyze** to extract summary, domain, and keywords
3. View results in a structured format

## 🔧 Supported File Formats
- **Plain Text** (`.txt`)
- **Microsoft Word** (`.doc`, `.docx`)
- **PDF Documents** (`.pdf`)
- **Rich Text Format** (`.rtf`)
- **OpenDocument Text** (`.odt`)
- **Markdown** (`.md`)

## 🛠 Technologies Used
- **Streamlit** - UI framework
- **Google Gemini AI** - Text analysis
- **Python Libraries** - `docx`, `fitz`, `pypandoc`, `markdown`

## 📩 Support
For issues or feature requests, reach out via:
- 📧 **Email:** [abi.developer123@gmail.com](mailto:abi.developer123@gmail.com)
- 🌍 **GitHub:** [View Repository](https://github.com/abinesh14/Document-Summarization)

## 📜 License
This project is open-source under the **MIT License**.

