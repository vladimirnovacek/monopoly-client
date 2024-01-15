
import tkinter as tk
import typing
from tkinter import ttk

from interfaces import Updatable, Conditions

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class RightMenu(tk.Frame, Updatable):

    def __init__(self, master: "GameWindow") -> None:
        super().__init__(master)
        self.master: "GameWindow" = master
        self.buttons: dict[str, ttk.Button] = {
            "roll": ttk.Button(self, text="Roll dice", command=self.roll),
            "move": ttk.Button(self, text="Move piece", command=self.move),
            "end_turn": ttk.Button(self, text="End turn", command=self.end_turn)
        }
        for button in self.buttons.values():
            button.configure(state=tk.DISABLED)
            button.pack(side=tk.TOP)

    def get_conditions(self) -> set[Conditions]:
        conditions = {
            Conditions(self.update_value, section="players", attribute="possible_actions")
        }
        conditions.update(super().get_conditions())
        return conditions

    def update_value(self, section, item, attribute, value):
        if section == "players" and attribute == "possible_actions":
            if self.master.game_data.on_turn:
                for name, button in self.buttons.items():
                    if name in value:
                        button.configure(state=tk.NORMAL)
                    else:
                        button.configure(state=tk.DISABLED)

    def process_actions(self, data: set[str]):
        for button_name, button in self.buttons.items():
            if button_name in data:
                button.configure(state=tk.NORMAL)
            else:
                button.configure(state=tk.DISABLED)

    def roll(self):
        self.master.message_factory.send("roll")

    def move(self):
        pass

    def buy(self):
        pass

    def end_turn(self):
        pass
