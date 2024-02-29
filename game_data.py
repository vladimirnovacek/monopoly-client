
from typing import TypedDict, Any, overload
from uuid import UUID


class Field(TypedDict, total=False):
    field_id: int
    type: str
    owner: int


class Player(TypedDict, total=False):
    player_id: int
    name: str
    token: str
    cash: int
    field: int
    ready: bool


class Misc(TypedDict, total=False):
    state: str
    on_turn: int
    last_roll: tuple
    my_id: int
    my_uuid: UUID
    player_order: list[int]
    possible_actions: list


class GameData:
    """
    Stores and maintains the game data.
    """

    def __init__(self):
        self.fields: dict[int, Field] = {}
        self.players: dict[int, Player] = {}
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
        if (section, item, attribute) == ("fields", -1, "lenght"):
            return
        if attribute is not None:
            if item not in self[section]:
                self[section][item] = {}
            self[section][item][attribute] = value
        else:
            self[section][item] = value

    def get_id(self) -> int:
        if "my_id" not in self.misc:
            return -1
        return self.misc["my_id"]

    def get_uuid(self) -> UUID | None:
        if "my_uuid" not in self.misc:
            return None
        return self.misc["my_uuid"]
