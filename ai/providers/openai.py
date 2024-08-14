import openai
from .base_provider import BaseAPIProvider
import os
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class OpenAI_API(BaseAPIProvider):
    MODELS = {
        "gpt-4-turbo": {"name": "GPT-4 Turbo", "provider": "OpenAI", "max_tokens": 4096},
        "gpt-4": {"name": "GPT-4", "provider": "OpenAI", "max_tokens": 4096},
        "gpt-4o": {"name": "GPT-4o", "provider": "OpenAI", "max_tokens": 4096},
        "gpt-4o-mini": {"name": "GPT-4o mini", "provider": "OpenAI", "max_tokens": 16384},
        "gpt-3.5-turbo-0125": {"name": "GPT-3.5 Turbo", "provider": "OpenAI", "max_tokens": 4096},
    }

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")

    def set_model(self, model_name: str):
        if model_name not in self.MODELS.keys():
            raise ValueError("Invalid model")
        self.current_model = model_name

    def get_models(self) -> dict:
        if self.api_key is not None:
            return self.MODELS
        else:
            return {}

    def generate_response(self, prompt: str, system_content: str) -> str:
        try:
            self.client = openai.OpenAI(api_key=self.api_key)
            response = self.client.chat.completions.create(
                model=self.current_model,
                n=1,
                messages=[{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
                max_tokens=self.MODELS[self.current_model]["max_tokens"],
            )
            return response.choices[0].message.content
        except openai.APIConnectionError as e:
            logger.error(f"Server could not be reached: {e.__cause__}")
            raise e
        except openai.RateLimitError as e:
            logger.error(f"A 429 status code was received. {e}")
            raise e
        except openai.AuthenticationError as e:
            logger.error(f"There's an issue with your API key. {e}")
            raise e
        except openai.APIStatusError as e:
            logger.error(f"Another non-200-range status code was received: {e.status_code}")
            raise e
