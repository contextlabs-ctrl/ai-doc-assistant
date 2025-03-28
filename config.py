import streamlit as st
import os

class Config:
    HF_TOKEN = st.secrets.get("HF_TOKEN") or os.getenv("HF_TOKEN")
    OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

    LLM_MODELS = {
        "Zephyr (HuggingFace)": {
            "type": "huggingface",
            "api_url": "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
            "headers": {"Authorization": f"Bearer {HF_TOKEN}"}
        },
        "Falcon (HuggingFace)": {
            "type": "huggingface",
            "api_url": "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
            "headers": {"Authorization": f"Bearer {HF_TOKEN}"}
        },
        "DeepSeek (HuggingFace)": {  # <-- ADDED THIS
            "type": "huggingface",
            "api_url": "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-llm-7b-chat",
            "headers": {"Authorization": f"Bearer {HF_TOKEN}"}
        },
        "GPT-3.5 Turbo (OpenAI)": {
            "type": "openai",
            "api_url": "https://api.openai.com/v1/chat/completions",
            "headers": {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            "model_name": "gpt-3.5-turbo"
        }
    }
