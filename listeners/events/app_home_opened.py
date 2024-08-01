from logging import Logger
from ai.ai_utils.get_available_apis import get_available_apis
from slack_sdk import WebClient
from state_store.get_user_state import get_user_state


def app_home_opened_callback(event, logger: Logger, client: WebClient):
    if event["tab"] != "home":
        return

    # create a list of options for the dropdown menu each containing the model name and API
    options = [
        {
            "text": {"type": "plain_text", "text": f"{model_info['name']} ({model_info['api']})", "emoji": True},
            "value": f"{model_name} {model_info['api'].lower()}",
        }
        for model_name, model_info in get_available_apis().items()
    ]

    # retrieve user's state to determine if they already have a selected model
    user_state = get_user_state(event["user"])
    initial_option = None

    if user_state:
        initial_model = get_user_state(event["user"])[1]
        # set the initial option to the user's previously selected model
        initial_option = list(filter(lambda x: x["value"].startswith(initial_model), options))
    else:
        # add an empty option if the user has no previously selected model.
        options.append(
            {
                "text": {"type": "plain_text", "text": " ", "emoji": True},
                "value": "null",
            }
        )

    try:
        client.views_publish(
            user_id=event["user"],
            view_id=event["view"]["id"],
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "header",
                        "text": {"type": "plain_text", "text": "Welcome to Bolty's Home Page!", "emoji": True},
                    },
                    {"type": "divider"},
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [{"type": "text", "text": "Select an API", "style": {"bold": True}}],
                            }
                        ],
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "static_select",
                                "initial_option": initial_option[0] if initial_option else options[-1],
                                "options": options,
                                "action_id": "pick_an_api",
                            }
                        ],
                    },
                ],
            },
        )
    except Exception as e:
        logger.error(e)
