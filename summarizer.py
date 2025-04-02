import requests
import openai
from config import Config


class Summarizer:
    def __init__(self, model_choice):
        self.model_info = Config.LLM_MODELS.get(model_choice, {})
        self.model_type = self.model_info.get("type")
        self.api_url = self.model_info.get("api_url")
        self.headers = self.model_info.get("headers")
        self.model_name = self.model_info.get("model_name")

    def summarize(self, prompt):
        if self.model_type == "openai":
            return self._openai(prompt)
        elif self.model_type == "deepseek":
            return self._deepseek(prompt)
        elif self.model_type == "huggingface":
            return self._huggingface(prompt)
        else:
            return "Error: Unsupported model type."

    def _openai(self, prompt):
        openai.api_key = Config.OPENAI_API_KEY
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=500,
            )
            return response.choices[0].message.content.strip()
        except openai.AuthenticationError:
            return "Error: OpenAI authentication failed. Check your API key."
        except openai.RateLimitError:
            return "Error: OpenAI rate limit exceeded. Try again later."
        except openai.OpenAIError as e:
            return f"Error: OpenAI API error — {str(e)}"

    def _deepseek(self, prompt):
        try:
            data = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 500
            }
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.exceptions.RequestException as e:
            return f"Error: DeepSeek API request failed — {str(e)}"
        except KeyError:
            return "Error: Unexpected DeepSeek response format."

    def _huggingface(self, prompt):
        try:
            data = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 500,
                    "temperature": 0.5
                }
            }
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            if isinstance(result, dict) and result.get("error"):
                return f"Error: HuggingFace API error — {result['error']}"
            return result[0]["generated_text"].strip()
        except requests.exceptions.RequestException as e:
            return f"Error: HuggingFace API request failed — {str(e)}"
        except (KeyError, IndexError):
            return "Error: Unexpected HuggingFace response format."
