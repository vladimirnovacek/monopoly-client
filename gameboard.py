
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
        self.root = master
        self.configure(relief="solid", borderwidth=2)
        self.image_ids = {
            "background": self.create_image(
                0, 0, anchor=tk.NW, image=self.root.images["background"]),
            "chance": self.create_image(
                100, 100, anchor=tk.NW, image=self.root.images["chance"]),
            "cc": self.create_image(
                499, 499, anchor=tk.SE, image=self.root.images["cc"])
        }
        self.tokens: dict[int, int] = {}
        self.dice: Dice = Dice(self)
        self.dice.draw()

        self.field_coordinates = config.field_coordinates

        # self.card: dict[str, Card | PropertyCard] = {
        #     "chance_cc": ChanceCcCard(self),
        #     "street": StreetCard(self),
        #     "railroad": RailroadCard(self),
        #     "utility": UtilityCard(self)
        # }

    def start_game(self):
        for player_id, player in self.master.game_data.players.items():
            token = self.root.tokens[config.tokens.index(player["token"])]
            x, y = self.field_coordinates[player["field"]]
            token_id = self.create_image(x, y, anchor=tk.CENTER, image=token)
            self.tokens[player_id] = token_id
            self.begin_turn()

    def begin_turn(self):
        if self.root.game_data.get_id() == self.root.game_data.misc["on_turn"]:
            self.tag_bind("dice", "<Button-1>", self._roll)
        else:
            self.tag_unbind("dice", "<Button-1>")

    def get_field_coordinate(self, field: int) -> tuple[int, int]:
        return self.field_coordinates[field]

    def _roll(self, *args):
        self.root.messenger.send("roll")

    def _move(self, section, item, attribute, value):
        if not self.dice.animation_over:
            self.wait_variable(self.dice.animation_over_var)
