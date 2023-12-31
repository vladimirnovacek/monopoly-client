
from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
import typing

from interfaces import Updatable, Conditions

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class LeftMenu(ttk.Frame, Updatable):

    def __init__(self, master: GameWindow) -> None:
        super().__init__(master)
        self.frames: list[ttk.Frame] = [ttk.Frame(self) for _ in range(4)]
        self.data: dict = {
            "players": [
                {
                    "name": tk.StringVar(self),
                    "cash": tk.StringVar(self)
                } for _ in range(4)
            ]
        }
        self.name_labels = [tk.Label(self.frames[i], textvariable=self.data["players"][i]["name"]) for i in range(4)]
        self.cash_labels = [tk.Label(self.frames[i], textvariable=self.data["players"][i]["cash"]) for i in range(4)]

        for i in range(4):
            self.frames[i].pack()
            self.name_labels[i].pack()
            self.cash_labels[i].pack()

    def select(self, keys: typing.Iterable) -> tk.IntVar | tk.StringVar | tk.BooleanVar:
        item = self.data
        for key in keys:
            item = item[key]
        return item

    def get_conditions(self) -> set[Conditions]:
        conditions = {
            Conditions(self.update_value, section="players", attribute="name"),
            Conditions(self.update_value, section="players", attribute="cash"),
        }
        conditions.update(super().get_conditions())
        return conditions

    def update_value(self, *, section, item, attribute = None, value):
        keys = (section, item, attribute) if attribute else (section, item)
        if keys not in self:
            return
        if self.select(keys).get() != value:
            self.select(keys).set(value)

    def __contains__(self, item):
        if isinstance(item, typing.Iterable):
            try:
                value = self.data
                for i in item:
                    value = value[i]
            except (IndexError, KeyError):
                return False
            return True
