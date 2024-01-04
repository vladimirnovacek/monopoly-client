import pickle
import uuid
from typing import Literal, Optional, Any, TypedDict

from twisted.internet.protocol import Protocol

from game_data import GameData


class ServerMessage(TypedDict):
    section: Literal["fields", "players", "misc"]
    item: str | uuid.UUID
    attribute: Optional[str]
    value: Any


class MessageParser:
    """
    Parses messages from the server.
    """

    def __init__(self, game_data: GameData):
        self.game_data: GameData = game_data
        self.network: Protocol | None = None  # Assigned after successful connection

    def _message_priority(self, message):
        priority = {"roll": 100, "move": 80}
        item = message["item"]
        return priority.get(item, 0)

    def parse(self, data: bytes):
        """
        Parses a message from the server.
        :param data: The message to parse.
        :return:
        """
        message_list: list[ServerMessage] = sorted(pickle.loads(data), key=self._message_priority)
        for message in message_list:
            self.game_data.update(**message)

    def send(self, message: str):
        """
        Sends a message to the server.
        :param message: The message to send.
        :return:
        """
        # noinspection PyUnresolvedReferences
        self.network.send(pickle.dumps(message))
