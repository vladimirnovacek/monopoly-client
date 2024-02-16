
from typing import TypedDict, Any, overload
from uuid import UUID

from interfaces import Observer


class Field(TypedDict, total=False):
    field_id: int
    owner: int


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
        self.fields: list[Field] = []
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

    @property
    def on_turn(self) -> bool:
        if "on_turn" not in self.misc or "my_id" not in self.misc:
            return False
        if self.misc["on_turn"] == self.misc["my_id"]:
            return True
        return False

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
        if section == "events":
            return
        if (section, item, attribute) == ("fields", -1, "lenght"):
            self.fields = [{} for _ in range(value)]
        elif attribute is not None:
            self[section][item][attribute] = value
        else:
            self[section][item] = value

    def get_uuid(self):
        return self.misc["my_uuid"]
