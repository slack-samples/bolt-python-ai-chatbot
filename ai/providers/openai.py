import openai
from .base_provider import BaseProvider
import os
from logging import Logger


class OpenAI_API(BaseProvider):
    MODELS = {
        "gpt-4o": "GPT-4o",
        "gpt-4-turbo": "GPT-4 Turbo",
        "gpt-4": "GPT-4",
        "gpt-3.5-turbo": "GPT-3.5 Turbo",
    }
    # this is ooptional value -> background on why i used it
    BASELINE_MAX_TOKENS = 4096
    API_NAME = "OpenAI"

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def set_model(self, model_name: str):
        if model_name not in self.MODELS.keys():
            raise ValueError("Invalid model")
        self.current_model = model_name

    def get_models(self):
        if self.api_key is not None:
            return {self.API_NAME: self.MODELS}
        else:
            return None

    def generate_response(self, prompt: str, system_content: str) -> str:
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.current_model,
                n=1,
                messages=[{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
                max_tokens=self.BASELINE_MAX_TOKENS,
            )
            return response.choices[0].message.content
        except openai.APIConnectionError as e:
            Logger.error(f"Server could not be reached: {e.__cause__}")
        except openai.RateLimitError as e:
            Logger.error(f"A 429 status code was received. Your account has hit a rate limit. {e}")
        except openai.AuthenticationError as e:
            Logger.error(f"There's an issue with your API key. {e}")
        except openai.APIStatusError as e:
            Logger.error(f"Another non-200-range status code was received: {e.status_code}")


"""
MODELS={
   "gpt-4-turbo": {name: "GPT-4 Turbo", model: "OpenAI", model_type: "gpt-4o"}
}
"""
