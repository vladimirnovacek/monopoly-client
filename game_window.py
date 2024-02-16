
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

        self.not_selected_token = ImageTk.PhotoImage(Image.open("resources/tokens/not_selected.png"))
        self.tokens: list[ImageTk.PhotoImage] = [
            ImageTk.PhotoImage(file=token) for token in config.tokens
        ]
        self.images: dict[str, ImageTk.PhotoImage] = {
            "board": ImageTk.PhotoImage(file="resources/board.png"),
        }

        # game control
        self.messenger: Messenger = messenger
        self.messenger.game = self
        self.game_data: GameData = game_data


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

    def parse(self, **message):
        logging.debug(f"Parsing event: {message['item']}")
        match message["item"]:
            case "initialize":
                self._retrieve_board_data()
                self._retrieve_my_data()
                self._add_player(self.game_data["misc"]["my_id"])

    def update_value(self, section, item, attribute, value):
        for condition in self._conditions:
            condition.call(section=section, item=item, attribute=attribute, value=value)

    def destroy(self):
        self.game_data.unregister(self)
        super().destroy()

    def _retrieve_board_data(self):
        for message in self.messenger.message["fields"]:
            self.game_data.update(
                section="fields", item=message["item"], attribute=message["attribute"], value=message["value"]
            )

    def _retrieve_my_data(self):
        for message in self.messenger.message["misc"]:
            self.game_data.update(
                section="misc", item=message["item"], value=message["value"]
            )

    def _add_player(self, player_id: int):
        for message in self.messenger.message["players"]:
            if player_id == message["item"]:
                self.game_data.update(
                    section="players", item=message["item"], attribute=message["attribute"], value=message["value"]
                )
        self.right_menu.add_player(self.game_data.players[player_id])
