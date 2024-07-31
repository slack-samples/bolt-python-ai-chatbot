from slack_bolt import App
from .set_user_selection import set_user_selection


def register(app: App):
    app.action("pick_an_api")(set_user_selection)
