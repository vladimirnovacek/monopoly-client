
import tkinter as tk
from tkinter import ttk


class RightMenu(tk.Frame):

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
