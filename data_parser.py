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
        priority = {
            -1: 0, # section=fields, item -1 marks board info(e.g. board lenght)
            "roll": 10,
            "move": 20,
            "on_turn": 30
        }
        item = message["item"]
        return priority.get(item, 999)

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
