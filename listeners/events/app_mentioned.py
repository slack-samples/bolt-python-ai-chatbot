from ai.ai_utils.handle_response import get_ai_response
from logging import Logger
from slack_sdk import WebClient
from slack_bolt import Say
from ..listener_utils.listener_constants import DEFAULT_LOADING_TEXT, MENTION_WITHOUT_TEXT
from ..listener_utils.parse_conversation import parse_conversation


# what does this function do
def app_mentioned_callback(client: WebClient, event, logger: Logger, say: Say):
    try:
        channel_id = event.get("channel")
        thread_ts = event.get("thread_ts")
        user_id = event.get("user")
        bot_id = client.auth_test()["user_id"]
        text = event.get("text")

        if thread_ts:
            conversation = client.conversations_replies(channel=channel_id, ts=thread_ts, limit=20)["messages"]
        else:
            conversation = client.conversations_history(channel=channel_id, limit=20)["messages"]
            thread_ts = event["ts"]

        conversation_context = parse_conversation(conversation, bot_id)

        if text:
            waiting_message = say(text=DEFAULT_LOADING_TEXT, thread_ts=thread_ts)
            response = get_ai_response(user_id, text, conversation_context)
            client.chat_update(channel=channel_id, ts=waiting_message["ts"], text=response)
        else:
            response = MENTION_WITHOUT_TEXT
            say(text=response, thread_ts=thread_ts)

    except Exception as e:
        logger.error(e)


# why use say vs respond
