from .create_file import FileStateStore, UserIdentity


def set_user_state(user_id: str, api_name: str, model_name: str):
    try:
        user = UserIdentity(user_id=user_id, api=api_name, model=model_name)
        file_store = FileStateStore()
        file_store.set_state(user)
    except Exception as e:
        raise ValueError(f"Error instantiating API: {e}")
