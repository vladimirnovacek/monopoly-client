
from abc import ABC, abstractmethod
from typing import Protocol


class Observer(ABC):
    @abstractmethod
    def update_value(self, section, item, attribute, value):
        ...


class Parser(Protocol):
    def parse(self, data: bytes):
        ...
