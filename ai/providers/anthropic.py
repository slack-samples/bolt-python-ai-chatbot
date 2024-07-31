from .base_provider import BaseProvider
import anthropic
import os
from logging import Logger


class AnthropicAPI(BaseProvider):
    MODELS = {
        "claude-3-5-sonnet-20240620": "Claude 3.5 Sonnet",
        "claude-3-sonnet-20240229": "Claude 3 Sonnet",
        "claude-3-haiku-20240307": "Claude 3 Haiku",
        "claude-3-opus-20240229": "Claude 3 Opus",
    }
    # this is ooptional value -> background on why i used it, link to token usage
    BASELINE_MAX_TOKENS = 10000
    API_NAME = "Anthropic"

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

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
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.current_model,
                max_tokens=1000,
                system=system_content,
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            )
            return response.content[0].text
        except anthropic.APIConnectionError as e:
            Logger.error(f"Server could not be reached: {e.__cause__}")
        except anthropic.RateLimitError as e:
            Logger.error(f"A 429 status code was received. Your account has hit a rate limit. {e}")
        except anthropic.AuthenticationError as e:
            Logger.error(f"There's an issue with your API key. {e}")
        except anthropic.APIStatusError as e:
            Logger.error(f"Another non-200-range status code was received: {e.status_code}")
