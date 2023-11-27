from twisted.internet.protocol import ClientFactory, Protocol

from interfaces import Parser
from message_factory import MessageFactory


class Client(Protocol):
    factory: "ClFactory"

    def dataReceived(self, data: bytes):
        self.factory.parser.parse(data)

    def connectionMade(self):
        self.factory.parser.network = self
        self.factory.message_factory.network = self

    def send(self, data: bytes):
        self.transport.write(data)


class ClFactory(ClientFactory):
    protocol = Client

    def __init__(self, parser: Parser, message_factory: MessageFactory):
        self.parser: Parser = parser
        self.message_factory: MessageFactory = message_factory
