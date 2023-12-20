
from __future__ import annotations

import tkinter as tk
import typing

import config
# from GUI.card import Card, PropertyCard
# from GUI.chance_cc_card import ChanceCcCard
# from GUI.dice import Dice
# from GUI.railroad_card import RailroadCard
# from GUI.street_cards import StreetCard
# from GUI.utility_card import UtilityCard

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class GameBoard(tk.Canvas):

    def __init__(self,
                 master: GameWindow = None,
                 width=config.board_size["width"],
                 height=config.board_size["height"],
    ) -> None:
        super().__init__(master, width=width, height=height)
        self.master: GameWindow = master
        self.images = {
            "background": tk.PhotoImage(master=self, file=config.path_board_image),
            "chance": tk.PhotoImage(master=self, file=config.path_chance_image),
            "cc": tk.PhotoImage(master=self, file=config.path_cc_image)
        }
        self.ids = {
            "background": self.create_image(
                0, 0, anchor=tk.NW, image=self.images["background"]),
            "chance": self.create_image(
                100, 100, anchor=tk.NW, image=self.images["chance"]),
            "cc": self.create_image(
                499, 499, anchor=tk.SE, image=self.images["cc"])
        }
        self.field_coordinates = config.field_coordinates

        # self.dice: Dice = Dice()  # kostky
        # self.dice.draw(self)  # immediately draw the dice on board
        # self.card: dict[str, Card | PropertyCard] = {
        #     "chance_cc": ChanceCcCard(self),
        #     "street": StreetCard(self),
        #     "railroad": RailroadCard(self),
        #     "utility": UtilityCard(self)
        # }

    def get_field_coordinate(self, field: int) -> tuple[int, int]:
        return self.field_coordinates[field]
