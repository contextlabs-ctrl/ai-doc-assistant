
# 🤖 AI Document Assistant

An intelligent, multi-purpose document interaction tool powered by Large Language Models (LLMs). Built with Streamlit for demonstration and educational use.

## 🔍 What It Does

This tool lets you:
- ✅ Upload a PDF, DOCX, or TXT document or paste a URL
- ✅ Choose between **Summarization** or **Question Answering (Q&A)**
- ✅ Select document type and use-case for customized prompt handling
- ✅ Choose your preferred LLM backend: GPT-3.5 (OpenAI), DeepSeek, Falcon, or Zephyr
- ✅ View output, download results, and understand how the system works

## 🎯 Use Cases

| Document Type      | Use Case Examples                     |
|--------------------|----------------------------------------|
| Business Report    | Executive brief, internal memo        |
| Academic Article   | Research summary, Q&A with citations   |
| Internal Policy    | Summarize procedures, extract rules    |
| Marketing Proposal | Bullet points for client handoff       |

## 🛠️ Technologies Used

- **Streamlit** for frontend
- **LangChain-style prompt customization**
- **Hugging Face Inference API**, **OpenAI API**, **DeepSeek API**
- `pdfplumber`, `docx`, `BeautifulSoup` for document processing

## 🧠 Architecture

```
User Upload ➡️ Document Extractor ➡️ Prompt Builder ➡️ LLM Engine ➡️ Output Viewer
```

- `document_reader.py`: Reads and cleans document
- `prompt_builder.py`: Builds dynamic prompt based on task/type/use
- `summarizer.py`: Routes request to chosen LLM
- `app.py`: UI logic

## 🧩 Setup Instructions

1. Clone the repo
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.streamlit/secrets.toml` (do NOT commit this):
   ```toml
   HF_TOKEN = "your_huggingface_token"
   OPENAI_API_KEY = "your_openai_api_key"
   DEEPSEEK_API_KEY = "your_deepseek_api_key"
   ```
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## 🔐 Privacy Notice

- No uploaded files are stored or logged.
- All content is processed temporarily and securely in-memory.
- API keys are managed securely through Streamlit Cloud secrets.

## 📜 Terms & Conditions

By using this demo, you agree to:
- Uploaded content is processed temporarily and not stored or shared.
- Results are AI-generated and may contain inaccuracies.
- The developer is not liable for actions taken based on outputs.
- Access and features may change or be limited without notice.
- Commercial use of demo outputs is prohibited.

## 📧 Contact & Collaboration

Built by ContextLabs | **ali@contextlabs.dev**  
Currently available for freelance & full-time AI/NLP roles.

**Portfolio/Demo**: [https://contextlabs.dev](https://contextlabs.dev)
