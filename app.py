import streamlit as st
from document_reader import DocumentReader
from summarizer import Summarizer
from prompt_builder import PromptBuilder
from config import Config

# --- Page setup ---
st.set_page_config(page_title="AI Document Assistant", layout="wide")
st.title("📄 AI Document Assistant")
st.markdown("Upload a document and use AI to summarize or ask questions — powered by multiple LLMs.")

# --- Sidebar Controls ---
st.sidebar.header("🧩 Control Panel")

# Demo mode toggle (to protect API usage)
demo_mode = st.sidebar.checkbox("Enable Demo Mode (no API cost)", value=True)


# File Upload
upload_type = st.sidebar.radio("Input Type", ["Upload File", "Enter URL"])
uploaded_file = None
url = ""

if upload_type == "Upload File":
    uploaded_file = st.sidebar.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
elif upload_type == "Enter URL":
    url = st.sidebar.text_input("Paste URL here")

# Task selection
task = st.sidebar.selectbox("Select Task", ["Summarize", "Ask Question"])
doc_type = st.sidebar.selectbox("Document Type", ["Business Report", "Academic Article", "Internal Policy", "Marketing Copy"])
use_case = st.sidebar.selectbox("Use Case", ["Executive Brief", "Internal Memo", "Client Delivery", "Legal Review"])
model_choice = st.sidebar.selectbox("LLM Model", list(Config.LLM_MODELS.keys()))

# Optional: Question input (for Q&A mode)
question = ""
if task == "Ask Question":
    question = st.sidebar.text_input("Your Question")

run_button = st.sidebar.button("🚀 Run Task")

# --- Main Area ---
content = ""
if uploaded_file or url:
    content = DocumentReader.extract_content(upload_type, uploaded_file if uploaded_file else url)
    content = content.strip()
    if len(content) > 4000:
        content = content[:4000] + "\n...[truncated]"

if content:
    st.subheader("📄 Extracted Content")
    st.text_area("Preview", content, height=180)

if run_button and content:
    prompt_builder = PromptBuilder(task=task.lower(), doc_type=doc_type, use_case=use_case)
    prompt = (
        prompt_builder.generate((question, content)) if task == "Ask Question"
        else prompt_builder.generate(content)
    )

    if demo_mode:
        st.info("Running in Demo Mode: This is a placeholder response.")
        result = "This is a demo response. Contact ali@contextlabs.dev for the full version with real LLM outputs."
    else:
        with st.spinner(f"Running {task} using {model_choice}..."):
            result = Summarizer.summarize(prompt, style="Custom", model_choice=model_choice)

        if result.lower().startswith("error"):
            st.error("Model temporarily unavailable. Try again or select another model.")

    st.subheader("✅ Result")
    st.markdown(result)
    st.download_button("⬇️ Download Result", result.encode("utf-8"), file_name="result.txt", mime="text/plain")

# --- System Explanation ---
st.markdown("---")
st.subheader("📊 How This Assistant Works")

col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://via.placeholder.com/300x250.png?text=AI+Process+Diagram")  # Replace with your real diagram

with col2:
    st.markdown("""
**Step-by-step process:**
1. You upload a file or paste a URL.
2. You select your goal — summarize or ask a question.
3. You describe the document type and your use case.
4. The system generates a customized prompt.
5. Your selected LLM processes the prompt and generates a response.
6. You review and download the result.

No data is stored. Your content is processed temporarily and only shown to you.
    """)

st.markdown("""
---
### 🔒 Privacy Note
Your document is processed securely in-memory only. No content is stored or shared.

### ⚠️ Extraction Limitations
Scanned PDFs or complex layouts may not extract cleanly.

### 📌 Output Disclaimer
Outputs are AI-generated and should be verified before critical use.

### 📜 Terms & Conditions
By using this demo, you agree:
- Data is temporarily processed; not stored/shared.
- AI-generated results may contain inaccuracies.
- Developer is not liable for actions based on outputs.
- Commercial use of demo outputs is prohibited.

Built by ContextLabs | [ali@contextlabs.dev](mailto:ali@contextlabs.dev)  
Interested in a tailored AI tool? [Contact me](mailto:ali@contextlabs.dev).
""")
