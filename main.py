
from twisted.internet import tksupport, reactor

import config
from data_parser import MessageParser
from client import ClFactory
from game_data import GameData
from lobby import Lobby
from message_factory import MessageFactory


def start():
    """
    Starts the application.
    :return:
    """
    game_data = GameData()
    message_factory = MessageFactory(game_data)
    root = Lobby(message_factory, game_data)
    root.protocol("WM_DELETE_WINDOW", reactor.stop)
    tksupport.install(root)
    reactor.connectTCP(config.server_address, config.server_port, ClFactory(MessageParser(game_data), message_factory))
    reactor.run()


if __name__ == '__main__':
    start()
