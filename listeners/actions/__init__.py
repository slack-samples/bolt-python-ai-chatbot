from slack_bolt import App
from .set_user_selection import set_user_selection


def register(app: App):
    app.action("pick_a_provider")(set_user_selection)
