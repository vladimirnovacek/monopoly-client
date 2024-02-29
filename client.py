import logging
import pickle
from typing import Any

from twisted.internet.protocol import ClientFactory, Protocol

import config
from messenger import Messenger


class Client(Protocol):
    factory: "ClFactory"

    def dataReceived(self, data: bytes):
        messages = config.encoder.decode(data)
        for message in messages:
            log = f"Received data: \n"
            for i in message:
                log += f"{i}\n"
            logging.debug(log[:-2])
            self.factory.messenger.parse(message)

    def connectionMade(self):
        self.factory.messenger.network = self

    def send(self, message: Any):
        logging.debug(f"Sending data: {message}")
        # noinspection PyArgumentList
        self.transport.write(config.encoder.encode(message))


class ClFactory(ClientFactory):
    protocol = Client

    def __init__(self, messenger: Messenger):
        self.messenger: Messenger = messenger
