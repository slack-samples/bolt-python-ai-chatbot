from .anthropic import AnthropicAPI
from .openai import OpenAI_API
from ..ai_constants import DEFAULT_SYSTEM_CONTENT
from state_store.get_user_state import get_user_state
from typing import Optional, List

"""
New AI providers must be added below.

`get_available_providers()`
This function retrieves available API models from different AI providers.
It combines the available models into a single dictionary.

`_get_provider()`
This function returns an instance of the appropriate API provider based on the given provider name.

`get_provider_response`()
This function retrieves the user's selected API provider and model,
sets the model, and generates a response.
Note that context is an optional parameter because some functionalities,
such as commands, do not allow access to conversation history if the bot
isn't in the channel where the command is run.

"""


def get_available_providers():
    return {**AnthropicAPI().get_models(), **OpenAI_API().get_models()}


def _get_provider(provider_name: str):
    if provider_name.lower() == "openai":
        return OpenAI_API()
    elif provider_name.lower() == "anthropic":
        return AnthropicAPI()
    else:
        raise ValueError(f"Unknown provider: {provider_name}")


def get_provider_response(user_id: str, prompt: str, context: Optional[List] = [], system_content=DEFAULT_SYSTEM_CONTENT):
    formatted_context = "\n".join([f"{msg['user']}: {msg['text']}" for msg in context])
    full_prompt = f"Prompt: {prompt}\nContext: {formatted_context}"
    try:
        provider_name, model_name = get_user_state(user_id)
        provider = _get_provider(provider_name)
        provider.set_model(model_name)
        return provider.generate_response(full_prompt, system_content)
    except Exception as e:
        return f"{e}"
