from typing import TypedDict


class UserIdentity(TypedDict):
    user_id: str
    provider: str
    model: str
