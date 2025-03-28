import requests
from config import Config

class Summarizer:
    STYLES = {
        "Bullet points (concise)": "Summarize the following in concise bullet points:",
        "Detailed paragraph": "Provide a detailed paragraph summary of the following:",
        "Executive summary (formal)": "Provide a professional executive summary of the following:"
    }

    @staticmethod
    def summarize(text, style, model_choice):
        prompt = f"{Summarizer.STYLES[style]}\n\n{text}\n\nSummary:"
        model_config = Config.LLM_MODELS[model_choice]

        if model_config["type"] == "huggingface":
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": 600}}
            response = requests.post(
                model_config["api_url"],
                headers=model_config["headers"],
                json=payload
            )
            if response.status_code == 200:
                output = response.json()[0]['generated_text']
                return output.split("Summary:")[-1].strip()
            else:
                return f"Error: {response.status_code} - {response.text}"

        elif model_config["type"] == "openai":
            payload = {
                "model": model_config["model_name"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            response = requests.post(
                model_config["api_url"],
                headers=model_config["headers"],
                json=payload
            )
            if response.status_code == 200:
                output = response.json()
                return output["choices"][0]["message"]["content"].strip()
            else:
                return f"Error: {response.status_code} - {response.text}"

        else:
            return "Unsupported model selected."
