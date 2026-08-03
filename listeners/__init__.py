from listeners import actions, commands, events, functions


def register_listeners(app):
    actions.register(app)
    commands.register(app)
    events.register(app)
    functions.register(app)
