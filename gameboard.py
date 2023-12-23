
from __future__ import annotations

import tkinter as tk
import typing
from os import path

from PIL import Image, ImageTk

import config
from interfaces import Observer

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class GameBoard(tk.Canvas, Observer):

    def __init__(
            self,
            master: GameWindow = None,
            width=config.board_size["width"],
            height=config.board_size["height"],
    ) -> None:
        super().__init__(master, width=width, height=height)
        self.images = {
            "background": ImageTk.PhotoImage(Image.open(path.join(config.path_images, "board.png"))),
            "chance": ImageTk.PhotoImage(Image.open(path.join(config.path_images, "chance.png"))),
            "cc": ImageTk.PhotoImage(Image.open(path.join(config.path_images, "cc.png")))
        }
        self.ids = {
            key: self.create_image(0, 0, anchor=tk.NW, image=image) for key, image in self.images.items()
        }
        self.tokens = {}
        self.field_coordinates = config.field_coordinates

        # self.dice: Dice = Dice()  # kostky
        # self.dice.draw(self)  # immediately draw the dice on board
        # self.card: dict[str, Card | PropertyCard] = {
        #     "chance_cc": ChanceCcCard(self),
        #     "street": StreetCard(self),
        #     "railroad": RailroadCard(self),
        #     "utility": UtilityCard(self)
        # }

    def update_value(self, section, item, attribute, value):
        pass
        # if (section, item, value) == ("misc", "state", "begin_turn")

    def get_field_coordinate(self, field: int) -> tuple[int, int]:
        return self.field_coordinates[field]
