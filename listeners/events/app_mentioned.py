from ai.providers import get_provider_response
from logging import Logger
from slack_sdk import WebClient
from slack_bolt import Say
from ..listener_utils.listener_constants import (
    DEFAULT_LOADING_TEXT,
    MENTION_WITHOUT_TEXT,
)
from ..listener_utils.parse_conversation import parse_conversation

"""
Handles the event when the app is mentioned in a Slack channel, retrieves the conversation context,
and generates an AI response if text is provided, otherwise sends a default response
"""


def app_mentioned_callback(client: WebClient, event: dict, logger: Logger, say: Say):
    try:
        channel_id = event.get("channel")
        thread_ts = event.get("thread_ts")
        user_id = event.get("user")
        text = event.get("text")

        if thread_ts:
            conversation = client.conversations_replies(
                channel=channel_id, ts=thread_ts, limit=10
            )["messages"]
        else:
            conversation = client.conversations_history(channel=channel_id, limit=10)[
                "messages"
            ]
            thread_ts = event["ts"]

        conversation_context = parse_conversation(conversation[:-1])

        if text:
            waiting_message = say(text=DEFAULT_LOADING_TEXT, thread_ts=thread_ts)
            response = get_provider_response(user_id, text, conversation_context)
            client.chat_update(
                channel=channel_id, ts=waiting_message["ts"], text=response
            )
        else:
            response = MENTION_WITHOUT_TEXT
            client.chat_update(
                channel=channel_id, ts=waiting_message["ts"], text=response
            )

    except Exception as e:
        logger.error(e)
        client.chat_update(
            channel=channel_id,
            ts=waiting_message["ts"],
            text=f"Received an error from Bolty:\n{e}",
        )
