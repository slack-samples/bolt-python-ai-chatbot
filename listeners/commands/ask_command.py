from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from ai.ai_utils.handle_response import get_ai_response


def ask_callback(ack: Ack, command, say: Say, logger: Logger, context: BoltContext):
    try:
        ack()
        user_id = context["user_id"]
        prompt = command["text"]
        if prompt == "":
            say(text="Please provide a question.")
        else:
            say(text=get_ai_response(user_id, prompt))
    except Exception as e:
        logger.error(e)
