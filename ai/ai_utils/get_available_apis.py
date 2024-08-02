from ai.providers.anthropic import AnthropicAPI
from ai.providers.openai import OpenAI_API

"""
This file defines a function to retrieve available API models from different AI providers.
It imports specific AI provider classes and combines their available models into a single dictionary.

New AI providers must be added below
"""


def get_available_apis():
    return {**AnthropicAPI().get_models(), **OpenAI_API().get_models()}
