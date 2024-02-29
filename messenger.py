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
            ("event", "initialize"),
            ("event", "player_connected"),
            ("event", "possible_actions"),
        ]
        if (message["section"], message["item"]) in priority:
            return priority.index((message["section"], message["item"]))
        else:
            return 999

    def parse(self, message: list):
        """
        Parses a message from the server.
        :param message: The message to parse.
        :type message: list
        :return:
        """
        self.message = message
        # TESTING PURPOSES ONLY, REMOVE LATER
        if self.game.game_data.my_id in (-1, 0):
            with open("messages.txt", "a") as f:
                f.write(f"{message}\n")
        # END OF TESTING BLOCK
        if event := self.find(section="event"):
            self.game.parse(event)

    def send(self, action: str, parameters: dict[str, Any] = None):
        if parameters is None:
            parameters = {}
        message = {
            "my_uuid": self.uuid,
            "action": action,
            "parameters": parameters
        }
        self.network.send(message)

    def find(self, **kwargs) -> dict | None:
        result = self.message[::-1]
        for key, value in kwargs.items():
            result = [message for message in result if message[key] == value]
        return result[0] if result else None
