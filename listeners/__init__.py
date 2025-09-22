from listeners import assistant
from listeners import actions
from listeners import commands
from listeners import events
from listeners import functions


def register_listeners(app):
    assistant.register(app)
    actions.register(app)
    commands.register(app)
    events.register(app)
    functions.register(app)
