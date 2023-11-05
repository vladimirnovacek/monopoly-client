from threading import Thread

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
        self.message_parser = MessageParser(self.game_data)

    def start(self):
        self.game_data.register(self.root)
        self.root.protocol("WM_DELETE_WINDOW", reactor.stop)
        tksupport.install(self.root)
        reactor.connectTCP(config.server_address, config.server_port, ClFactory(self.message_parser))
        reactor.run()


def prompt(app: MainApp):
    while True:
        i = input("Zadej vstup")
        app.message_parser.send(i)

def start_client():
    app = MainApp()
    t = Thread(target=prompt, args=(app,))
    t.start()
    app.start()


if __name__ == '__main__':
    start_client()
