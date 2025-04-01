import requests
import openai
from config import Config

class Summarizer:
    def __init__(self, model_choice):
        self.model_info = Config.LLM_MODELS[model_choice]
        self.api_url = self.model_info["api_url"]
        self.headers = self.model_info["headers"]
        self.model_type = self.model_info["type"]
        self.model_name = self.model_info.get("model_name", None)

    def summarize(self, prompt):
        try:
            if self.model_type == "openai":
                return self._openai_request(prompt)
            elif self.model_type == "deepseek":
                return self._deepseek_request(prompt)
            elif self.model_type == "huggingface":
                return self._huggingface_request(prompt)
            else:
                return "Model type not supported."
        except Exception as e:
            return f"Error: {str(e)}"

    def _openai_request(self, prompt):
        openai.api_key = Config.OPENAI_API_KEY
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except openai.error.RateLimitError:
            return "OpenAI API rate limit exceeded. Try again later."
        except openai.error.AuthenticationError:
            return "OpenAI authentication failed. Verify your API key."
        except openai.error.OpenAIError as e:
            return f"OpenAI API Error: {str(e)}"

    def _deepseek_request(self, prompt):
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 500
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data, timeout=15)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.exceptions.HTTPError as e:
            return f"DeepSeek HTTP Error: {str(e)}"
        except requests.exceptions.Timeout:
            return "DeepSeek API timeout. Please retry shortly."
        except requests.exceptions.RequestException as e:
            return f"DeepSeek Request Error: {str(e)}"

    def _huggingface_request(self, prompt):
        data = {
            "inputs": prompt,
            "parameters": {"max_length": 500, "temperature": 0.5},
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data, timeout=15)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, dict) and result.get('error'):
                return f"HuggingFace API Error: {result['error']}"
            return result[0]['generated_text'].strip()
        except requests.exceptions.HTTPError as e:
            return f"HuggingFace HTTP Error: {str(e)}"
        except requests.exceptions.Timeout:
            return "HuggingFace API timeout. Please retry shortly."
        except requests.exceptions.RequestException as e:
            return f"HuggingFace Request Error: {str(e)}"
