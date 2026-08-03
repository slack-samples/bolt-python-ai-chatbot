import json
import logging
import os
from pathlib import Path

from .user_identity import UserIdentity
from .user_state_store import UserStateStore

_logger = logging.getLogger(__name__)


class FileStateStore(UserStateStore):
    def __init__(
        self,
        *,
        base_dir: str = "./data",
        logger: logging.Logger = _logger,
    ):
        self.base_dir = base_dir
        self.logger = logger

    def set_state(self, user_identity: UserIdentity):
        state = user_identity["user_id"]
        self._mkdir(self.base_dir)
        filepath = f"{self.base_dir}/{state}"

        with open(filepath, "w") as file:
            data = json.dumps(user_identity)
            file.write(data)
        return state

    def unset_state(self, user_identity: UserIdentity):
        state = user_identity["user_id"]
        filepath = f"{self.base_dir}/{state}"
        try:
            os.remove(filepath)
            return state
        except FileNotFoundError as e:
            self.logger.warning(f"Failed to find data for {user_identity} - {e}")
            raise

    @staticmethod
    def _mkdir(path):
        if isinstance(path, str):
            path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
