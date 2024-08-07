from .user_identity import UserIdentity


class UserStateStore:
    def set_state(user_identity: UserIdentity):
        raise NotImplementedError()

    def unset_state(state: str):
        raise NotImplementedError()
