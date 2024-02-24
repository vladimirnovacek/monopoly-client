
from __future__ import annotations

import logging
import os
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

import config
from interfaces import Updatable
from gameboard import GameBoard

from game_data import GameData
from messenger import Messenger
from rightmenu import RightMenu


class GameWindow(tk.Tk, Updatable):

    def __init__(self, messenger: Messenger, game_data: GameData) -> None:
        super().__init__()

        # images
        self.not_selected_token = ImageTk.PhotoImage(Image.open("resources/tokens/not_selected.png"))
        self.tokens: list[ImageTk.PhotoImage] = [
            ImageTk.PhotoImage(
                file=os.path.join(config.path_tokens, f"{token}.png")
            ) for token in config.tokens
        ]
        self.images: dict[str, ImageTk.PhotoImage] = {
            "background": ImageTk.PhotoImage(file=os.path.join(config.path_images, "board.png")),
            "chance": ImageTk.PhotoImage(file=os.path.join(config.path_images, "chance.png")),
            "cc": ImageTk.PhotoImage(file=os.path.join(config.path_images, "cc.png")),
            "left_arrow": ImageTk.PhotoImage(file=os.path.join(config.path_images, "buttons/left_arrow.png")),
            "right_arrow": ImageTk.PhotoImage(file=os.path.join(config.path_images, "buttons/right_arrow.png")),
        }

        # game control
        self.messenger: Messenger = messenger
        self.messenger.game = self
        self.game_data: GameData = game_data

        # Window drawing
        self.geometry("1280x720")
        self.title("Monopoly")
        self.resizable(False, False)

        self.style = ttk.Style()

        self.game_board: GameBoard = GameBoard(self)
        self.game_board.grid(row=0, column=0, padx=60, pady=60, sticky="nsew")

        self.right_menu = RightMenu(self, padding=10)
        self.right_menu.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(1, weight=1)

    def parse(self, message):
        logging.debug(f"Parsing event: {message['item']}")
        match message["item"]:
            case "initialize":
                self._retrieve_data()
                for player_id in self.game_data["players"].keys():
                    self._add_player(player_id)
            case "player_updated":
                self._retrieve_data()
            case "player_connected":
                self._retrieve_data()
                self._add_player(message["value"])
            case "game_started":
                self._retrieve_data()
                self.right_menu.start_game()
                self.game_board.start_game()
            case "roll":
                self.game_board.dice.roll(message["value"])
                while not self.game_board.dice.animation_over_var.get():
                    self.wait_variable(self.game_board.dice.animation_over_var)

    def _set_ready(self, *args):
        self.ready = True

    def _retrieve_data(self):
        for message in self.messenger.message:
            if message["section"] == "event":
                continue
            if "attribute" in message:
                self.game_data.update(
                    section=message["section"], item=message["item"], attribute=message["attribute"], value=message["value"]
                )
            else:
                self.game_data.update(
                    section=message["section"], item=message["item"], value=message["value"]
                )
            if message["section"] == "players":
                self.right_menu.update_player(message["item"], message["attribute"], message["value"])

    def _add_player(self, player_id: int):
        self.right_menu.add_player(player_id)
