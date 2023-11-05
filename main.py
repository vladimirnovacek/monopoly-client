
from twisted.internet import tksupport, reactor

import config
from data_parser import MessageParser
from client import ClFactory
from game_data import GameData
from lobby import Lobby


class MainApp:
    def __init__(self):
        self.root = Lobby()
        self.game_data = GameData()

    def start(self):
        self.game_data.register(self.root)
        self.root.protocol("WM_DELETE_WINDOW", reactor.stop)
        tksupport.install(self.root)
        r = reactor.connectTCP(config.server_address, config.server_port, ClFactory(MessageParser(self.game_data)))
        reactor.run()


def start_client():
    app = MainApp()
    app.start()


if __name__ == '__main__':
    start_client()
