from .ai_constants import DEFAULT_SYSTEM_CONTENT
from ai.providers.openai import OpenAI_API
from ai.providers.anthropic import AnthropicAPI
from logging import Logger
from state_store.get_user_state import get_user_state
from typing import Optional, List
from ..providers import _get_provider

"""
This file defines the `get_provider_response` function which retrieves the user's selected API provider and model,
sets the model, and generates a response.
"""


def get_provider_response(user_id: str, prompt: str, context: Optional[List] = None, system_content=DEFAULT_SYSTEM_CONTENT):
    try:
        formatted_context = "\n".join([f"{msg['user']}: {msg['text']}" for msg in context])
        full_prompt = f"Prompt: {prompt}\nContext: {formatted_context}"
        provider_name, model_name = get_user_state(user_id)
        provider = _get_provider(provider_name)
        provider.set_model(model_name)
        return provider.generate_response(full_prompt, system_content)
    except Exception as e:
        Logger.error(e)
