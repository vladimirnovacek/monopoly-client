
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

    FIELD_COORDINATES: typing.Final[list[tuple[int, int]]] = [
        (40, 40), (105, 25), (153, 25), (202, 25), (251, 25),
        (299, 25), (348, 25), (397, 25), (445, 25), (494, 25),
        (580, 25), (574, 105), (574, 153), (574, 202), (574, 251),
        (574, 299), (574, 348), (574, 397), (574, 445), (574, 494),
        (559, 559), (494, 574), (445, 574), (397, 574), (348, 574),
        (299, 574), (251, 574), (202, 574), (153, 574), (105, 574),
        (40, 559), (25, 494), (25, 445), (25, 397), (25, 348),
        (25, 299), (25, 251), (25, 202), (25, 153), (25, 105),
        (547, 52)
    ]
    """ List of coordinates of fields on the gameboard. Coordinates are of the
    center of the fields. Last tuple is coordinate of a jail"""

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

        # self.dice: Dice = Dice()  # kostky
        # self.dice.draw(self)  # immediately draw the dice on board
        # self.card: dict[str, Card | PropertyCard] = {
        #     "chance_cc": ChanceCcCard(self),
        #     "street": StreetCard(self),
        #     "railroad": RailroadCard(self),
        #     "utility": UtilityCard(self)
        # }

    def get_field_coordinate(self, field: int) -> tuple[int, int]:
        return self.FIELD_COORDINATES[field]
