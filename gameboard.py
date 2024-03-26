
from __future__ import annotations

import tkinter as tk
import typing
from time import sleep

import config
from dialogs.dialog import DeedDialog
from dice import Dice

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class GameBoard(tk.Canvas):
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

        self.token_field_positions = config.token_field_positions
        self.field_coordinates = config.field_coordinates

        self.bind("<Button-1>", self._canvas_clicked)

        # self.card: dict[str, Card | PropertyCard] = {
        #     "chance_cc": ChanceCcCard(self),
        #     "street": StreetCard(self),
        #     "railroad": RailroadCard(self),
        #     "utility": UtilityCard(self)
        # }

    def _canvas_clicked(self, event: tk.Event) -> None:
        x, y = event.x, event.y
        for i, field in enumerate(self.field_coordinates):
            x1, y1 = field[0]
            x2, y2 = field[1]
            if x1 <= x <= x2 and y1 <= y <= y2:
                print(f"Clicked field number {i}")
                if self.root.game_data.fields[i]['type'] in ('street', 'railroad', 'utility'):
                    dialog = DeedDialog.get_overview_dialog(self, self.root.game_data.fields[i])
                    self.root.show_dialog(dialog)
                return
        print("Clicked canvas")

    def moveto(self, tagOrId, x = 0, y = 0,
               anchor: typing.Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = tk.NW):
        x0, y0, x1, y1 = self.bbox(tagOrId)
        width, height = x1 - x0, y1 - y0
        deltas = {
            tk.NW: (0, 0), tk.N: (width / 2, 0), tk.NE: (width, 0),
            tk.W: (0, height / 2), tk.CENTER: (width / 2, height / 2), tk.E: (width, height / 2),
            tk.SW: (0, height), tk.S: (width / 2, height), tk.SE: (width, height)
        }
        dx, dy = deltas[anchor]

        super().moveto(tagOrId, x - dx, y - dy)

    def start_game(self):
        for player_id, player in self.master.game_data.players.items():
            token = self.root.tokens[config.tokens.index(player["token"])]
            x, y = self.token_field_positions[player["field"]]
            token_id = self.create_image(x, y, anchor=tk.CENTER, image=token)
            self.tokens[player_id] = token_id

    def begin_turn(self):
        if self.root.game_data.my_id == self.root.game_data.misc["on_turn"]:
            self.tag_bind("dice", "<Button-1>", self._roll)
        else:
            self.tag_unbind("dice", "<Button-1>")

    def _roll(self, *args):
        self.root.messenger.send("roll")

    def move_token(self, player_id: int, end_field_id: int, *, backwards: bool = False, directly: bool = False):
        def step(to_id: int):
            if backwards:
                from_id = 0 if to_id == len(self.token_field_positions) - 2 else to_id + 1
            else:
                from_id = len(self.token_field_positions) - 2 if to_id == 0 else to_id - 1
            x0, y0 = self.token_field_positions[from_id]
            x1, y1 = self.token_field_positions[to_id]
            dx, dy = x1 - x0, y1 - y0
            self.move(self.tokens[player_id], dx, dy)


        field_id = self.root.game_data.players[player_id]["field"]

        if directly:
            x, y = self.token_field_positions[end_field_id]
            self.moveto(self.tokens[player_id], x, y, anchor=tk.CENTER)
            return

        delay = 0.3
        if backwards:
            while field_id != end_field_id:
                field_id -= 1
                if field_id < 0:
                    field_id %= 40
                step(field_id)
                self.update()
                sleep(delay)
        else:
            while field_id != end_field_id:
                field_id += 1
                if field_id >= len(self.token_field_positions) - 1:
                    field_id %= len(self.token_field_positions) - 1
                step(field_id)
                self.update()
                sleep(delay)
