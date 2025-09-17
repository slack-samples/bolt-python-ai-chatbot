from .assistant import assistant

def register(app):
    # Using assistant middleware is the recommended way.
    app.assistant(assistant)
