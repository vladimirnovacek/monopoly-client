
from __future__ import annotations

import logging
import os
import time
import tkinter as tk
from tkinter import ttk

from PIL import ImageTk, Image

import config
from dialogs import BuyDialog
from interfaces import Updatable
from gameboard import GameBoard

from game_data import GameData, Field
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
                self.right_menu.update_game_log("Welcome to Monopoly!")
            case "player_updated":
                self._retrieve_data()
            case "player_connected":
                self._retrieve_data()
                player_id = self.messenger.find(section="players")["item"]
                self._add_player(player_id)
                self.right_menu.update_game_log(f"{self.game_data.players[player_id]['name']} connected.")
            case "game_started":
                self._retrieve_data()
                self.right_menu.start_game()
                self.game_board.start_game()
                self.right_menu.update_game_log("Game started.")
            case "begin_turn":
                self._retrieve_data()
                self.right_menu.begin_turn()
                self.game_board.begin_turn()
                self.right_menu.update_game_log(
                    f"{self.game_data.on_turn_player['name']}'s turn."
                )
            case "roll":
                roll = self.messenger.find(section="misc", item="roll")["value"]
                self.game_board.dice.roll(roll)
                while not self.game_board.dice.animation_over_var.get():
                    self.wait_variable(self.game_board.dice.animation_over_var)
                self.right_menu.update_game_log(
                    f"{self.game_data.on_turn_player['name']} rolled {roll[0]} and {roll[1]}."
                )
            case "moved":
                message = self.messenger.find(section="players", attribute="field")
                player_id = message["item"]
                self.game_board.move_token(
                    player_id, self.game_data.players[player_id]["field"], message["value"]
                )
                self._retrieve_data()
                field = self.game_data.fields[message["value"]]
                own = owned_by = ""
                if field["type"] in ("street", "utility", "railroad"):
                    if "owner" in field and field["owner"] is not None:
                        if field["owner"] == message["item"]:
                            own = "own "
                        elif field["owner"] == self.game_data.my_id:
                            owned_by = " owned by you"
                        else:
                            owned_by = f" owned by {self.game_data.players[field['owner']]['name']}"
                log = f"{self.game_data.players[player_id]['name']} landed on {own}{field['name']}{owned_by}."
                self.right_menu.update_game_log(log)
            case "buying_decision":
                self._retrieve_data()
                player_id = self.game_data.misc["on_turn"]
                field_id = self.game_data.players[player_id]["field"]
                field = self.game_data.fields[field_id]
                if "buy" in self.game_data.misc["possible_actions"]:
                    self._show_dialog(BuyDialog, field)
                else:
                    self._show_dialog(BuyDialog, field, ())
            case "property_bought":
                self._retrieve_data()
                self.right_menu.update_game_log(
                    f"{self.game_data.on_turn_player['name']} bought {self.game_data.on_turn_player_field['name']} "
                    f"for £ {self.messenger.find(section='misc', item='price')['value']}"
                )
                self.dialog.show_sold()
                self.dialog.destroy()
            case "auction":
                self._retrieve_data()
                self.right_menu.update_game_log(
                    f"{self.game_data.on_turn_player['name']} did not buy {self.game_data.on_turn_player_field['name']}"
                )
                time.sleep(2)
                self.dialog.destroy()
            case "rent_paid":
                self._retrieve_data()
            case "end_turn":
                self._retrieve_data()
                # self.right_menu.btn_end_turn.configure(state=tk.NORMAL)

        if self.messenger.find(section="misc", item="possible_actions") is not None:
            self._set_control_states()

    def _set_control_states(self):
        if "possible_actions" not in self.game_data.misc:
            self._retrieve_data()
        self.right_menu.set_control_states()

    def _show_dialog(self, dialog_class: type[BuyDialog], field: Field, options: tuple = ("buy", "auction")):
        self.dialog: BuyDialog = dialog_class(self.game_board, field, options)
        self.dialog.place(relx=0.5, rely=0.4, anchor="center")
        self.dialog.show()

    def _set_ready(self, *args):
        self.ready = True

    def _retrieve_data(self):
        for message in self.messenger.message:
            if message["section"] == "event":
                continue
            self.game_data.update(**message)
            if message["section"] == "players":
                self.right_menu.update_player(message["item"], message["attribute"], message["value"])

    def _add_player(self, player_id: int):
        self.right_menu.add_player(player_id)
