import pickle

from twisted.internet.protocol import ClientFactory, Protocol

from messenger import Messenger


class Client(Protocol):
    factory: "ClFactory"

    def dataReceived(self, data: bytes):
        print(f"Received data: ")
        for i in pickle.loads(data):
            print(i)
        self.factory.messenger.parse(data)

    def connectionMade(self):
        self.factory.messenger.network = self

    def send(self, data: bytes):
        print(f"Sending data: {pickle.loads(data)}")
        # noinspection PyArgumentList
        self.transport.write(data)


class ClFactory(ClientFactory):
    protocol = Client

    def __init__(self, messenger: Messenger):
        self.messenger: Messenger = messenger
