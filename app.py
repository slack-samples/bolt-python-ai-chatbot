import os
import logging

from slack_bolt import App, Assistant
from slack_bolt.adapter.socket_mode import SocketModeHandler

from listeners import register_listeners

# Initialization
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
assistant = Assistant()
app.use(assistant)
logging.basicConfig(level=logging.DEBUG)

# Register Listeners
register_listeners(app)

# Start Bolt app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()
