import pickle

from game_data import GameData


class MessageParser:
    def __init__(self, game_data: GameData):
        self.game_data = game_data
        self.network = None

    def parse(self, data: bytes):
        print(f"Received message: {pickle.loads(data)}")

    def send(self, message: str):
        self.network.send(pickle.dumps(message))
