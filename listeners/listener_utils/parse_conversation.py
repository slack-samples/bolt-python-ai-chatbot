from logging import Logger


# What does this function do, what files use it?
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
