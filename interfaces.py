
from abc import ABC, abstractmethod
from typing import Protocol, Any, Callable


class Observer(ABC):
    @abstractmethod
    def update_value(self, section, item, attribute, value):
        ...


class Conditions:

    def __init__(self, method: Callable, pass_conditions: bool = True, **conditions):
        self.method: Callable = method
        self.pass_conditions: bool = pass_conditions
        self.conditions: dict[str, Any] = conditions

    def eval(self, **kwargs) -> bool:
        for key, value in self.conditions.items():
            equals = True
            if key.startswith("not__"):
                key = key.lstrip("not__")
                equals = False
            if key not in kwargs:
                return False
            if (value != kwargs[key]) == equals:
                return False
        return True

    def call(self, evaluate: bool = True, **kwargs):
        if evaluate and not self.eval(**kwargs):
            return
        if not self.pass_conditions:
            self.method()
        else:
            self.method(**kwargs)


class Control(ABC):
    @abstractmethod
    def activate(self):
        ...

    @abstractmethod
    def deactivate(self):
        ...


class Updatable:

    subclasses: set["Updatable"] = set()
    _conditions: set[Conditions] = set()

    def get_conditions(self) -> set[Conditions]:
        conditions = set()
        for child in self.subclasses:
            conditions.update(child.get_conditions())
        return conditions


class Parser(Protocol):
    def parse(self, data: bytes):
        ...
