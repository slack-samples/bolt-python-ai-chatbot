from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.providers import get_provider_response
from slack_sdk import WebClient

"""
Callback for handling the 'ask-bolty' command. It acknowledges the command, retrieves the user's ID and prompt,
checks if the prompt is empty, and responds with either an error message or the provider's response.
"""


def ask_callback(
    client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext
):
    try:
        ack()
        user_id = context["user_id"]
        channel_id = context["channel_id"]
        prompt = command["text"]

        if prompt == "":
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="Looks like you didn't provide a prompt. Try again.",
            )
        else:
            client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                blocks=[
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_quote",
                                "elements": [{"type": "text", "text": prompt}],
                            },
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": get_provider_response(user_id, prompt),
                                    }
                                ],
                            },
                        ],
                    }
                ],
            )
    except Exception as e:
        logger.error(e)
        client.chat_postEphemeral(
            channel=channel_id, user=user_id, text=f"Received an error from Bolty:\n{e}"
        )
