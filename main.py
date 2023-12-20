
from twisted.internet import tksupport, reactor

import config
from data_parser import MessageParser
from client import ClFactory
from game_data import GameData
from game_window import GameWindow
from message_factory import MessageFactory


def start():
    """
    Starts the application.
    :return:
    """
    game_data = GameData()
    message_factory = MessageFactory(game_data)
    game_window = GameWindow(message_factory, game_data)
    # noinspection PyUnresolvedReferences
    game_window.protocol("WM_DELETE_WINDOW", reactor.stop)
    tksupport.install(game_window)
    # noinspection PyUnresolvedReferences
    reactor.connectTCP(config.server_address, config.server_port, ClFactory(MessageParser(game_data), message_factory))
    # noinspection PyUnresolvedReferences
    reactor.run()


if __name__ == '__main__':
    start()
