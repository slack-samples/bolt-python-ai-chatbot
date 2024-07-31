from ai.providers.anthropic import AnthropicAPI
from ai.providers.openai import OpenAI_API

"""
New providers need to be added below
"""


def get_available_apis():
    return {**AnthropicAPI().get_models(), **OpenAI_API().get_models()}
