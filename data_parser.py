import pickle

from twisted.internet.protocol import Protocol

from game_data import GameData


class MessageParser:
    """
    Parses messages from the server.
    """

    def __init__(self, game_data: GameData):
        self.game_data: GameData = game_data
        self.network: Protocol | None = None  # Assigned after successful connection

    def parse(self, data: bytes):
        """
        Parses a message from the server.
        :param data: The message to parse.
        :return:
        """
        message_list = pickle.loads(data)
        print(f"Received message: {message_list}")
        for message in message_list:
            self.game_data.update(**message)

    def send(self, message: str):
        """
        Sends a message to the server.
        :param message: The message to send.
        :return:
        """
        self.network.send(pickle.dumps(message))
