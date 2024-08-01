from slack_bolt import App
from .summary_function import handle_summary_function_callback


def register(app: App):
    app.function("summary_function")(handle_summary_function_callback)
