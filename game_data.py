
from typing import TypedDict, Any, overload
from uuid import UUID

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
    state: str
    on_turn: int
    last_roll: tuple
    my_id: int
    my_uuid: UUID
    players_order: list[int]


class GameData:
    """
    Stores and maintains the game data.
    """

    def __init__(self):
        self.observers: list[Observer] = []  # TODO could be a set
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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def register(self, observer: Observer):
        """
        Registers an observer. The observer will be notified when the game data changes.
        :param observer:
        :return:
        """
        self.observers.append(observer)

    def unregister(self, observer: Observer):
        self.observers.remove(observer)

    @overload
    def update(self, *, section: str, item: str | int, value: Any):
        ...

    @overload
    def update(self, *, section: str, item: str | int, attribute: str, value: Any):
        ...

    def update(self, *, section: str, item: UUID | int, attribute: str | Any = None, value: Any):
        """
        Updates the game data and notifies the observers.
        :param section:
        :param item:
        :param attribute:
        :param value:
        :return:
        """
        for observer in self.observers:
            observer.update_value(section=section, item=item, attribute=attribute, value=value)
        if attribute is not None:
            self[section][item][attribute] = value
        else:
            self[section][item] = value

    def get_uuid(self):
        return self.misc["my_uuid"]

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