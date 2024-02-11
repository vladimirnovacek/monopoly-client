
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk

from interfaces import Updatable, Conditions, Observer
from gameboard import GameBoard

from game_data import GameData
from message_factory import MessageFactory
from rightmenu import RightMenu


class GameWindow(tk.Tk, Observer, Updatable):

    def __init__(self, message_factory: MessageFactory, game_data: GameData) -> None:
        super().__init__()
        self.geometry("1280x720")
        self.title("Monopoly")
        # self.resizable(False, False)
        self.message_factory: MessageFactory = message_factory
        self.game_data: GameData = game_data
        self.game_data.register(self)
        self.tokens: list[str] = [
            "resources/tokens/car.png",
            "resources/tokens/hat.png",
            "resources/tokens/thimble.png",
            "resources/tokens/wheelbarrow.png",
        ]
        self.images: dict[str, ImageTk.PhotoImage] = {
            "board": ImageTk.PhotoImage(file="resources/board.png"),
        }

        self.game_board: GameBoard = GameBoard(self)
        self.game_board.grid(row=0, column=0, padx=60, pady=60, sticky="nsew")

        self.right_menu = RightMenu(self, padding=10)
        self.right_menu.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)

    def draw_lobby(self):
        pass

    def get_conditions(self) -> set[Conditions]:
        conditions = {
            Conditions(self.deiconify, False, section="events", item="game_started"),
            Conditions(self.withdraw, False, section="misc", item="state", value="pregame"),
        }
        conditions.update(super().get_conditions())
        return conditions
        
    def update_value(self, section, item, attribute, value):
        for condition in self._conditions:
            condition.call(section=section, item=item, attribute=attribute, value=value)

    def destroy(self):
        self.game_data.unregister(self)
        super().destroy()