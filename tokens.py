import tkinter as tk
import typing
from os import path

from PIL import Image, ImageTk

import config
if typing.TYPE_CHECKING:
    from gameboard import GameBoard
from interfaces import Observer


class Token(Observer):

    def __init__(self, master: "GameBoard", player_id: int, name: str):
        self.master: "GameBoard" = master
        self.player_id: int = player_id
        self.image: ImageTk.PhotoImage = ImageTk.PhotoImage(
            Image.open(path.join(config.path_images, "tokens", f"{name}.png"))
        )
        self.canvas_id: int = -1
        self.field: int = -1
        self.master.master.game_data.register(self)

    def place(self, field: int = 0) -> None:
        x, y = self.master.get_field_coordinate(field)
        if self.canvas_id == -1:
            self.canvas_id = self.master.create_image(
                x, y, anchor=tk.CENTER, image=self.image)

    def update_value(self, section, item, attribute, value):
        if (section, item, attribute) == ("players", self.player_id, "field"):
            self.place(value)

    def move(self, field: int) -> None:
        if self.canvas_id == -1:
            self.place(field)
        self.field = field
        x2, y2 = self.master.get_field_coordinate(self.field)
        x1, y1 = self.master.coords(self.canvas_id)
        self.master.move(self.canvas_id, x2 - x1, y2 - y1)

    def remove(self) -> None:
        self.board.delete(self.canvas_id)
        self.canvas_id = -1
