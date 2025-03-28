import streamlit as st
import requests
import PyPDF2
import io
import os

# Page setup
st.set_page_config(page_title="LLM Document Summarizer (DeepSeek)", layout="centered")
st.title("🧠 LLM Document Summarizer")
st.write("Upload a PDF or TXT file and get a bullet-point summary using DeepSeek LLM.")

# Hugging Face API configuration
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

HF_TOKEN = st.secrets["HF_TOKEN"] if "HF_TOKEN" in st.secrets else os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Function to read uploaded file
def read_file(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return ""

# Function to call DeepSeek for summarization
def summarize_with_deepseek(text):
    prompt = f"Please summarize the following document in bullet points:\n\n{text}\n\nSummary:"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 512}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        output = response.json()
        return output[0]["generated_text"].split("Summary:")[-1].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Reading file..."):
        content = read_file(uploaded_file)
        content = content.strip()
        if len(content) > 4000:
            content = content[:4000] + "\n...[truncated]"

    st.subheader("Document Preview")
    st.text_area("File Content", content, height=200)

    if st.button("Summarize"):
        with st.spinner("Summarizing with DeepSeek..."):
            summary = summarize_with_deepseek(content)
        st.subheader("Summary")
        st.markdown(summary)
