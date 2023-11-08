from twisted.internet.protocol import ClientFactory, Protocol

from interfaces import Parser


class Client(Protocol):
    factory: "ClFactory"

    def dataReceived(self, data: bytes):
        self.factory.parser.parse(data)

    def connectionMade(self):
        self.factory.parser.network = self

    def send(self, data: bytes):
        self.transport.write(data)


class ClFactory(ClientFactory):
    protocol = Client

    def __init__(self, parser: Parser):
        self.parser: Parser = parser
