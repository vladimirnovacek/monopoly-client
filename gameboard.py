
from __future__ import annotations

import tkinter as tk
import typing
from os import path

from PIL import Image, ImageTk

import config
from dice import Dice
from interfaces import Updatable, Conditions
from tokens import Token

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class GameBoard(tk.Canvas, Updatable):
    master: GameWindow

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
            "background": self.create_image(
                0, 0, anchor=tk.NW, image=self.images["background"]),
            "chance": self.create_image(
                100, 100, anchor=tk.NW, image=self.images["chance"]),
            "cc": self.create_image(
                499, 499, anchor=tk.SE, image=self.images["cc"])
        }
        self.tokens: dict[int, Token] = {}
        self.dice: Dice = Dice(self)
        self.dice.draw()

        self.field_coordinates = config.field_coordinates

        # self.card: dict[str, Card | PropertyCard] = {
        #     "chance_cc": ChanceCcCard(self),
        #     "street": StreetCard(self),
        #     "railroad": RailroadCard(self),
        #     "utility": UtilityCard(self)
        # }


    def get_conditions(self):
        conditions = {
            Conditions(self.update_value, section="players", attribute="token"),
            Conditions(self._roll, section="misc", item="last_roll"),
            Conditions(self._move, section="players", attribute="field")
        }
        conditions.update(super().get_conditions())
        return conditions

    def update_value(self, section, item, attribute, value):
        if (section, attribute) == ("players", "token") and value != "":
            self.tokens[item] = Token(self, item, value)

    def get_field_coordinate(self, field: int) -> tuple[int, int]:
        return self.field_coordinates[field]

    def _roll(self, section, item, attribute, value):
        self.dice.roll(value)

    def _move(self, section, item, attribute, value):
        if not self.dice.animation_over:
            self.wait_variable(self.dice.animation_over_var)
        token = self.tokens[item]
        token.move(value)