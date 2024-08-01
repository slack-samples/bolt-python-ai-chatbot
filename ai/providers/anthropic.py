from .base_provider import BaseProvider
import anthropic
import os
from logging import Logger


class AnthropicAPI(BaseProvider):
    MODELS = {
        "claude-3-5-sonnet-20240620": {
            "name": "Claude 3.5 Sonnet",
            "api": "Anthropic",
            "max_tokens": 4096,  # or 8192 with the header anthropic-beta: max-tokens-3-5-sonnet-2024-07-15
        },
        "claude-3-sonnet-20240229": {"name": "Claude 3 Sonnet", "api": "Anthropic", "max_tokens": 4096},
        "claude-3-haiku-20240307": {"name": "Claude 3 Haiku", "api": "Anthropic", "max_tokens": 4096},
        "claude-3-opus-20240229": {"name": "Claude 3 Opus", "api": "Anthropic", "max_tokens": 4096},
    }

    def __init__(self):
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")

    def set_model(self, model_name: str):
        if model_name not in self.MODELS.keys():
            raise ValueError("Invalid model")
        self.current_model = model_name

    def get_models(self):
        if self.api_key is not None:
            return self.MODELS
        else:
            return None

    def generate_response(self, prompt: str, system_content: str) -> str:
        try:
            client = anthropic.Anthropic(api_key=self.api_key)
            response = client.messages.create(
                model=self.current_model,
                system=system_content,
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
                max_tokens=self.MODELS[self.current_model]["max_tokens"],
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