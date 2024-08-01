from logging import Logger


# Parses a conversation history, excluding messages from the bot,
# and formats it as a string with user IDs and their messages.
# Used in `app_mentioned_callback`, `dm_sent_callback`,
# and `handle_summary_function_callback`.
def parse_conversation(conversation: str, bot_id: str = ""):
    parsed = ""
    try:
        for message in conversation:
            user = message.get("user")
            text = message.get("text", "")
            if user != bot_id:
                parsed += f"{user}: {text}, "
        return str(parsed)
    except Exception as e:
        Logger.error(e)
        return None
