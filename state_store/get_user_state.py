import json
import os
from logging import Logger
from state_store.user_identity import UserIdentity


def get_user_state(user_id: str):
    filepath = f"./data/{user_id}"
    if not os.path.exists(filepath):
        raise FileNotFoundError("No provider selection found. Please navigate to the App Home and make a selection.")
    try:
        with open(filepath, "r") as file:
            user_identity: UserIdentity = json.load(file)
            return user_identity["provider"], user_identity["model"]
    except Exception as e:
        Logger.error(e)
        raise e
