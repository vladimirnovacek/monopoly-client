
import tkinter as tk
from tkinter import ttk

from interfaces import Updatable, Conditions


class RightMenu(tk.Frame, Updatable):

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master)
        self.master: tk.Tk = master
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
            Conditions(self.update_value, section="events", item="possible_actions")
        }
        conditions.update(super().get_conditions())
        return conditions

    def update_value(self, section, item, attribute, value):
        pass

    def process_actions(self, data: set[str]):
        for button_name, button in self.buttons.items():
            if button_name in data:
                button.configure(state=tk.NORMAL)
            else:
                button.configure(state=tk.DISABLED)

    def roll(self):
        pass

    def move(self):
        pass

    def buy(self):
        pass

    def end_turn(self):
        pass
