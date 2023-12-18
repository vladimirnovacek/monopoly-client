
from __future__ import annotations

import tkinter as tk
import tkinter.ttk as ttk
import typing

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class LeftMenu(ttk.Frame):

    def __init__(self, master: GameWindow) -> None:
        super().__init__(master)
        self.frames: list[ttk.Frame] = [ttk.Frame(self) for _ in range(4)]
        self.data: dict = dict()
        self.cash_vars = [tk.StringVar(self) for _ in range(4)]
        self.name_labels = [tk.Label(self.frames[i]) for i in range(4)]
        self.cash_labels = [
            tk.Label(self.frames[i], textvariable=self.cash_vars[i])
            for i in range(4)]

        for i in range(4):
            self.frames[i].pack()
            self.name_labels[i].pack()
            self.cash_labels[i].pack()
