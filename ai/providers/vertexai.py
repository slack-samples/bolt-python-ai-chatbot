import google.api_core.exceptions

from .base_provider import BaseAPIProvider
import os
import logging
import vertexai.generative_models

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class VertexAPI(BaseAPIProvider):
    VERTEX_AI_PROVIDER = "VertexAI"
    MODELS = {
        "gemini-1.5-flash-001": {
            "name": "Gemini 1.5 Flash 001",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-1.5-flash-002": {
            "name": "Gemini 1.5 Flash 002",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-1.5-pro-002": {
            "name": "Gemini 1.5 Pro 002",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-1.5-pro-001": {
            "name": "Gemini 1.5 Pro 001",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-1.0-pro-002": {
            "name": "Gemini 1.0 Pro 002",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-1.0-pro-001": {
            "name": "Gemini 1.0 Pro 001",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-flash-experimental": {
            "name": "Gemini Flash Experimental",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-pro-experimental": {
            "name": "Gemini Pro Experimental",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
        "gemini-experimental": {
            "name": "Gemini Pro Experimental",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 8192,
        },
    }

    def __init__(self):
        self.enabled = os.environ.get("VERTEX_AI_ENABLED", "").lower() in ["1", "true", "t", "yes", "y"]
        vertexai.init(project=os.environ.get("GCP_PROJECT"), location=os.environ.get("GCP_LOCATION"))

    def set_model(self, model_name: str):
        if model_name not in self.MODELS.keys():
            raise ValueError("Invalid model")
        self.current_model = model_name

    def get_models(self) -> dict:
        if self.enabled:
            return self.MODELS
        else:
            return {}

    def generate_response(self, prompt: str, system_content: str) -> str:
        try:
            self.client = vertexai.generative_models.GenerativeModel(
                model_name=self.current_model,
                system_instruction=system_content,
                generation_config={
                    "max_output_tokens": self.MODELS[self.current_model]["max_tokens"],
                },
            )
            response = self.client.generate_content(
                contents=prompt,
            )
            return "".join(part.text for part in response.candidates[0].content.parts)

        except google.api_core.exceptions.Unauthorized as e:
            logger.error(f"Client is not Authorized. {e.reason}, {e.message}")
            raise e
        except google.api_core.exceptions.Forbidden as e:
            logger.error(f"Client Forbidden. {e.reason}, {e.message}")
            raise e
        except google.api_core.exceptions.TooManyRequests as e:
            logger.error(f"A 429 status code was received. {e.reason}, {e.message}")
            raise e
        except google.api_core.exceptions.ClientError as e:
            logger.error(f"Client error: {e.reason}, {e.message}")
            raise e
        except google.api_core.exceptions.ServerError as e:
            logger.error(f"Server error: {e.reason}, {e.message}")
            raise e
        except google.api_core.exceptions.GoogleAPICallError as e:
            logger.error(f"Error: {e.reason}, {e.message}")
            raise e
        except google.api_core.exceptions.GoogleAPIError as e:
            logger.error(f"Unknown error.")
            raise e
