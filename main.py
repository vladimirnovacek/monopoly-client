
from twisted.internet import tksupport, reactor

import config
from client import ClFactory
from game_data import GameData
from game_window import GameWindow
from messenger import Messenger


def start():
    """
    Starts the application.
    :return:
    """
    game_data = GameData()
    message_factory = Messenger()
    game_window = GameWindow(message_factory, game_data)
    # noinspection PyUnresolvedReferences
    game_window.protocol("WM_DELETE_WINDOW", reactor.stop)
    tksupport.install(game_window)
    # noinspection PyUnresolvedReferences
    reactor.connectTCP(config.server_address, config.server_port, ClFactory(message_factory))
    # noinspection PyUnresolvedReferences
    reactor.run()


if __name__ == '__main__':
    start()
