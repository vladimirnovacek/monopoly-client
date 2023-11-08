from typing import Protocol


class Observer(Protocol):
    def update(self, section, item, attribute, value):
        ...


class Parser(Protocol):
    def parse(self, data: bytes):
        ...
