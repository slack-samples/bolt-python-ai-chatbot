from ai.ai_utils.handle_response import get_ai_response
from logging import Logger
from slack_bolt import Complete, Fail, Ack
from slack_sdk import WebClient
from ..listener_utils.listener_constants import SUMMARIZE_CHANNEL_WORKFLOW
from ..listener_utils.parse_conversation import parse_conversation


# Handles the event to summarize a Slack channel's conversation history.
# It retrieves the conversation history, parses it, generates a summary using an AI response,
# and completes the workflow with the summary or fails if an error occurs.
def handle_summary_function_callback(
    ack: Ack, inputs: dict, fail: Fail, logger: Logger, client: WebClient, complete: Complete
):
    ack()
    try:
        user_context = inputs["user_context"]
        channel_id = inputs["channel_id"]
        history = client.conversations_history(channel=channel_id, limit=20)["messages"]
        conversation = parse_conversation(history)

        summary = get_ai_response(user_context["id"], SUMMARIZE_CHANNEL_WORKFLOW, conversation)

        complete({"user_context": user_context, "response": summary})
    except Exception as e:
        logger.exception(e)
        fail(e)
