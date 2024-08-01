# This file defines constant messages used by the Slack bot for when a user mentions the bot without text,
# when summarizing a channel's conversation history, and a default loading message.
# Used in `app_mentioned_callback`, `dm_sent_callback`, and `handle_summary_function_callback`.

MENTION_WITHOUT_TEXT = """
Hi there! You didn't provide a message with your mention.
    Mention me again in this thread so that I can help you out!
"""
SUMMARIZE_CHANNEL_WORKFLOW = """
User has just joined this slack channel.
Create a quick summary the most recent messages in this channel to cath up the user.
"""
DEFAULT_LOADING_TEXT = "Thinking..."
