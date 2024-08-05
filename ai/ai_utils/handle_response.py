from .ai_constants import DEFAULT_SYSTEM_CONTENT
from ai.providers.openai import OpenAI_API
from ai.providers.anthropic import AnthropicAPI
from logging import Logger
from state_store.get_user_state import get_user_state

"""
This file defines functions to handle AI responses by interacting with different AI providers.
The `_get_provider()` function returns an instance of the appropriate API provider based on the given API name. 
The `get_ai_response` function retrieves the user's selected API provider and model, sets the model, and generates a response.

New AI providers must be added below
"""


def _get_provider(api_name: str):
    if api_name.lower() == "openai":
        return OpenAI_API()
    if api_name.lower() == "anthropic":
        return AnthropicAPI()


def get_ai_response(user_id: str, prompt: str, context: list = [], system_content=DEFAULT_SYSTEM_CONTENT):
    try:
        formatted_context = "\n".join([f"{msg['user']}: {msg['text']}" for msg in context])
        full_prompt = f"Prompt: {prompt}\nContext: {formatted_context}"
        api_name, model_name = get_user_state(user_id)
        provider = _get_provider(api_name)
        provider.set_model(model_name)
        return provider.generate_response(full_prompt, system_content)
    except Exception as e:
        Logger.error(e)
