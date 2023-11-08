import time
from threading import Thread

from twisted.internet import tksupport, reactor

import config
from data_parser import MessageParser
from client import ClFactory
from game_data import GameData
from lobby import Lobby


class MainApp:
    """
    Main application class.
    """
    def __init__(self):
        self.root = Lobby()
        self.game_data = GameData()
        self.message_parser = MessageParser(self.game_data)

    def start(self):
        """
        Starts the application.
        :return:
        """
        self.game_data.register(self.root.game_data)
        self.root.protocol("WM_DELETE_WINDOW", reactor.stop)
        tksupport.install(self.root)
        reactor.connectTCP(config.server_address, config.server_port, ClFactory(self.message_parser))
        reactor.run()


def prompt(app: MainApp):
    time.sleep(3)
    app.message_parser.send("start")

def start_client():
    app = MainApp()
    t = Thread(target=prompt, args=(app,))
    t.start()
    app.start()



if __name__ == '__main__':
    start_client()
