import os
import logging
from azure.core.credentials import AzureKeyCredential
from azure.ai.openai import OpenAIClient
from .base_provider import BaseAPIProvider

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class AzureAI_API(BaseAPIProvider):
    MODELS = {
        "gpt-4o": {"name": "GPT-4o", "provider": "AzureOpenAI", "max_tokens": 4096},
        "gpt-4o-mini": {"name": "GPT-4o mini", "provider": "AzureOpenAI", "max_tokens": 16384}
        # Following models in preview:
        # "o1-preview": {"name": "o1-preview", "provider": "AzureOpenAI", max_tokens: ""},
        # "o1-mini": {"name": "o1-mini", "provider": "AzureOpenAI", max_tokens: ""}
    }

    def __init__(self):
        self.api_key = os.environ.get("AZURE_API_KEY")
        self.endpoint = os.environ.get("AZURE_ENDPOINT")
        self.deployment_name = os.environ.get("AZURE_DEPLOYMENT_NAME")
        self.client = None
        if self.api_key and self.endpoint and self.deployment_name:
            self.client = OpenAIClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.api_key))

    def set_model(self, model_name: str):
        if model_name not in self.MODELS.keys():
            raise ValueError("Invalid model")
        self.current_model = model_name

    def get_models(self) -> dict:
        if self.api_key and self.endpoint and self.deployment_name:
            return self.MODELS
        else:
            return {}

    def generate_response(self, prompt: str, system_content: str) -> str:
        if not self.client:
            raise ValueError("Azure OpenAI client not properly configured. Ensure API key, endpoint, and deployment name are set.")

        try:
            response = self.client.chat_completions.create(
                deployment_id=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.MODELS[self.current_model]["max_tokens"]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error occurred while generating a response: {e}")
            raise e
