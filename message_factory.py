import pickle
from typing import Any, TYPE_CHECKING

import game_data

if TYPE_CHECKING:
    from client import Client


class MessageFactory:
    def __init__(self, data: game_data.GameData):
        self.game_data = data
        self.network: Client | None = None

    @property
    def uuid(self):
        return self.game_data.get_uuid()

    def get(self, action: str, parameters: dict[str, Any]) -> bytes:
        message = {
            "my_uuid": self.uuid,
            "action": action,
            "parameters": parameters
        }
        return pickle.dumps(message)

    def send(self, action: str, parameters: dict[str, Any]):
        message = self.get(action, parameters)
        self.network.send(message)