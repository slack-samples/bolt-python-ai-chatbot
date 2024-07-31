from ai.ai_utils.ai_constants import DM_SYSTEM_CONTENT
from ai.ai_utils.handle_response import get_ai_response
from logging import Logger
from slack_bolt import Say
from slack_sdk import WebClient
from ..listener_utils.listener_constants import DEFAULT_LOADING_TEXT
from ..listener_utils.parse_conversation import parse_conversation


# what does this do, whats using it
def dm_sent_callback(client: WebClient, event, logger: Logger, say: Say):
    channel_id = event.get("channel")
    thread_ts = event.get("thread_ts")
    user_id = event.get("user")
    text = event.get("text")

    try:
        if channel_id[0] == "D":
            conversation_context = ""

            if thread_ts:  # whats a thread, why does it get context
                conversation = client.conversations_replies(channel=channel_id, limit=20, ts=thread_ts)["messages"]
                conversation_context = parse_conversation(conversation)

            waiting_message = say(text=DEFAULT_LOADING_TEXT, thread_ts=thread_ts)
            response = get_ai_response(user_id, text, conversation_context, DM_SYSTEM_CONTENT)
            client.chat_update(channel=channel_id, ts=waiting_message["ts"], text=response)
    except Exception as e:
        logger.error(e)
