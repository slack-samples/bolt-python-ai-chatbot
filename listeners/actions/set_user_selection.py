from logging import Logger
from slack_bolt import Ack
from state_store.set_user_state import set_user_state


def set_user_selection(logger: Logger, ack: Ack, body: dict):
    try:
        ack()
        user_id = body["user"]["id"]
        value = body["actions"][0]["selected_option"]["value"]
        if value != "null":
            # explain how and why parsing action body
            selected_api, selected_model = value.split(" ")[-1], value.split(" ")[0]
            set_user_state(user_id, selected_api, selected_model)
        else:
            raise ValueError("Please make a selection")
    except Exception as e:
        logger.error(e)
