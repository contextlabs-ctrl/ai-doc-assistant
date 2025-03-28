import streamlit as st
from document_reader import DocumentReader
from summarizer import Summarizer
from config import Config

# Streamlit page config
st.set_page_config(page_title="KL LLM Summarizer", layout="centered")
st.title("🧠 KL LLM Summarizer")
st.subheader("Tailored Document Summarization Powered by AI")

# User input (no change)
upload_type = st.radio("Choose input type:", ["Upload File", "Enter URL"])

content = ""
if upload_type == "Upload File":
    uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])
    if uploaded_file:
        content = DocumentReader.extract_content(upload_type, uploaded_file)
elif upload_type == "Enter URL":
    url = st.text_input("Paste URL here:")
    if url:
        content = DocumentReader.extract_content(upload_type, url)

# Summarization style selector
style = st.selectbox("Select summarization style:", [
    "Bullet points (concise)",
    "Detailed paragraph",
    "Executive summary (formal)"
])

# LLM model selector (NEW!)
model_choice = st.selectbox("Choose LLM model:", list(Config.LLM_MODELS.keys()))

# Display extracted content
if content:
    if len(content) > 4000:
        content = content[:4000] + "\n...[truncated]"
    st.subheader("Content Preview")
    st.text_area("Extracted Content", content, height=150)

    if st.button("Summarize"):
        with st.spinner(f"Generating summary using {model_choice}..."):
            summary = Summarizer.summarize(content, style, model_choice)
        st.subheader("Generated Summary")
        st.markdown(summary)

        summary_bytes = summary.encode('utf-8')
        st.download_button("⬇️ Download Summary", data=summary_bytes,
                           file_name="summary.txt", mime="text/plain")

# Footer branding
st.markdown("---")
st.markdown("🚀 Built by **Your Name**, LLM Freelancer | Kuala Lumpur | [your.email@example.com](mailto:your.email@example.com)")
