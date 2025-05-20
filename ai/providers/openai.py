import openai
from .base_provider import BaseAPIProvider
import os
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class OpenAI_API(BaseAPIProvider):
    MODELS = {
        "gpt-4.1": {"name": "GPT-4.1", "provider": "OpenAI", "max_tokens": 10000},
        "gpt-4.1-mini": {"name": "GPT-4.1 Mini", "provider": "OpenAI", "max_tokens": 10000},
        "gpt-4.1-nano": {"name": "GPT-4.1 Nano", "provider": "OpenAI", "max_tokens": 10000},
        "o4-mini": {"name": "o4-mini", "provider": "OpenAI", "max_tokens": 50000},
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
            response = self.client.responses.create(
                model=self.current_model,
                input=[
                    {"role": "developer", "content": system_content},
                    {"role": "user", "content": prompt},
                ],
                max_output_tokens=self.MODELS[self.current_model]["max_tokens"],
            )
            return response.output_text
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
