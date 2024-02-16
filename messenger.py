import pickle
from typing import Any, TYPE_CHECKING, TypedDict, Literal, Optional
from uuid import UUID


if TYPE_CHECKING:
    from client import Client
    from game_window import GameWindow


class ServerMessage(TypedDict):
    section: Literal["fields", "players", "misc"]
    item: str | UUID
    attribute: Optional[str]
    value: Any


class Messenger:
    def __init__(self):
        self.game: GameWindow | None = None
        self.message: dict = {}
        self.network: Client | None = None

    @property
    def uuid(self):
        return self.game.game_data.get_uuid()

    def _message_priority(self, message):
        priority = [
            ("events", "initialize"),
            ("events", "player_connected"),
            ("events", "possible_actions"),
        ]
        if (message["section"], message["item"]) in priority:
            return priority.index((message["section"], message["item"]))
        else:
            return 999

    def parse(self, data: bytes):
        """
        Parses a message from the server.
        :param data: The message to parse.
        :return:
        """
        self.message = self.organize_messages(pickle.loads(data))
        for event in self.message["events"]:
            self.game.parse(section="events", item=event["item"], value=event["value"])

    def _get(self, action: str, parameters: dict[str, Any]) -> bytes:
        message = {
            "my_uuid": self.uuid,
            "action": action,
            "parameters": parameters
        }
        return pickle.dumps(message)

    def send(self, action: str, parameters: dict[str, Any] = None):
        if parameters is None:
            parameters = {}
        message = self._get(action, parameters)
        self.network.send(message)

    @staticmethod
    def organize_messages(messages):
        sorted_messages = {}
        for message in messages:
            section = message.pop("section")
            if section not in sorted_messages:
                sorted_messages[section] = []
            sorted_messages[section].append(message)
        return sorted_messages