from typing import Protocol


class Observer(Protocol):
    def update_data(self, section, item, attribute_or_value, value):
        ...


class Parser(Protocol):
    def parse(self, data: bytes):
        ...
