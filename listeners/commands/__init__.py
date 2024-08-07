from slack_bolt import App
from .ask_command import ask_callback


def register(app: App):
    app.command("/ask-bolty")(ask_callback)
