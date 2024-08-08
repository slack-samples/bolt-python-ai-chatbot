from .anthropic import AnthropicAPI
from .openai import OpenAI_API

"""
The `_get_provider()` function returns an instance of the appropriate API provider based on the given provider name.
New providers must be added below.
"""
def _get_provider(provider_name: str):
    if provider_name.lower() == "openai":
        return OpenAI_API()
    elif provider_name.lower() == "anthropic":
        return AnthropicAPI()
    else:
        raise ValueError(f"Unknown provider: {provider_name}")
