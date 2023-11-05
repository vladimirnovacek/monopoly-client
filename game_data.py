
from typing import TypedDict, Any, overload

from interfaces import Observer


class Field(TypedDict, total=False):
    field_id: int
    owner: int
    houses: int
    mortgage: bool


class Player(TypedDict, total=False):
    player_id: int
    name: str
    token: str
    cash: int
    field_id: int
    ready: bool


class Misc(TypedDict, total=False):
    on_turn: int
    last_roll: tuple
    my_id: int
    my_uuid: str
    players_order: list[int]


class GameData:

    def __init__(self):
        self.observers: list[Observer] = []
        self.fields: dict[int, Field] = {}
        self.players: list[Player] = [
            {"player_id": 0, "name": "", "token": "", "cash": 0, "field_id": -1, "ready": False},
            {"player_id": 1, "name": "", "token": "", "cash": 0, "field_id": -1, "ready": False},
            {"player_id": 2, "name": "", "token": "", "cash": 0, "field_id": -1, "ready": False},
            {"player_id": 3, "name": "", "token": "", "cash": 0, "field_id": -1, "ready": False}
        ]
        self.misc: Misc = {}

    def __getitem__(self, item):
        return getattr(self, item)

    def register(self, observer: Observer):
        self.observers.append(observer)

    @overload
    def set(self, section: str, item: str | int, value: Any):
        ...

    @overload
    def set(self, section: str, item: str | int, attribute: str, value: Any):
        ...

    def set(self, section: str, item: str | int, attribute_or_value: str | Any, value: Any = None):
        for observer in self.observers:
            observer.update_data(section, item, attribute_or_value, value)
        if value is not None:
            self[section][item][attribute_or_value] = value
        else:
            self[section][item] = attribute_or_value


'''
{"jmeno":
    {
        "player_id": 0,
        "name": "jmeno",
        "token": "car",
        "
    }
}
'''