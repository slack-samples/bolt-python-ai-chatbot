from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.providers import get_provider_response

"""
Callback for handling the 'ask-bolty' command. It acknowledges the command, retrieves the user's ID and prompt,
checks if the prompt is empty, and responds with either an error message or the provider's response.
"""


def ask_callback(ack: Ack, command, say: Say, logger: Logger, context: BoltContext):
    try:
        ack()
        user_id = context["user_id"]
        prompt = command["text"]
        if prompt == "":
            say(text="Please provide a question.")
        else:
            say(text=get_provider_response(user_id, prompt))
    except Exception as e:
        logger.error(e)
        say(text=f"Received an error from Bolty: {e}")
