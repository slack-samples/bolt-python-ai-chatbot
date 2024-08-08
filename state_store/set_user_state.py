from .file_state_store import FileStateStore, UserIdentity


def set_user_state(user_id: str, provider_name: str, model_name: str):
    try:
        user = UserIdentity(user_id=user_id, provider=provider_name, model=model_name)
        file_store = FileStateStore()
        file_store.set_state(user)
    except Exception as e:
        raise ValueError(f"Error instantiating API: {e}")
