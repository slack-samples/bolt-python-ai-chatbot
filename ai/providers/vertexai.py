import logging
import os
from typing import ClassVar

from google import genai
from google.genai import errors, types

from .base_provider import BaseAPIProvider

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class VertexAPI(BaseAPIProvider):
    VERTEX_AI_PROVIDER = "VertexAI"
    MODELS: ClassVar[dict] = {
        "gemini-3.5-flash-lite": {
            "name": "Gemini 3.5 Flash-Lite",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 16384,
            "system_instruction_supported": True,
        },
        "gemini-3.8-flash": {
            "name": "Gemini 3.8 Flash",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 16384,
            "system_instruction_supported": True,
        },
        "gemini-4-argon": {
            "name": "Gemini 4 Argon",
            "provider": VERTEX_AI_PROVIDER,
            "max_tokens": 16384,
            "system_instruction_supported": True,
        },
    }

    def __init__(self):
        self.enabled = bool(os.environ.get("VERTEX_AI_PROJECT_ID", ""))
        if self.enabled:
            self.client = genai.Client(
                enterprise=True,
                project=os.environ.get("VERTEX_AI_PROJECT_ID"),
                location=os.environ.get("VERTEX_AI_LOCATION"),
            )

    def set_model(self, model_name: str):
        if model_name not in self.MODELS:
            raise ValueError("Invalid model")
        self.current_model = model_name

    def get_models(self) -> dict:
        if self.enabled:
            return self.MODELS
        else:
            return {}

    def generate_response(self, prompt: str, system_content: str) -> str:
        system_instruction = None
        if self.MODELS[self.current_model]["system_instruction_supported"]:
            system_instruction = system_content
        else:
            prompt = system_content + "\n" + prompt

        try:
            response = self.client.models.generate_content(
                model=self.current_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=self.MODELS[self.current_model]["max_tokens"],
                    system_instruction=system_instruction,
                ),
            )
            return response.text

        except errors.ClientError as e:
            logger.error(f"Client error: {e.code} {e.status}, {e.message}")
            raise
        except errors.ServerError as e:
            logger.error(f"Server error: {e.code} {e.status}, {e.message}")
            raise
        except errors.APIError as e:
            logger.error(f"Error: {e.code} {e.status}, {e.message}")
            raise
