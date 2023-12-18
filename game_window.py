
from __future__ import annotations

import tkinter as tk

from interfaces import Observer
from gameboard import GameBoard
from leftmenu import LeftMenu
from lobby import Lobby
from rightmenu import RightMenu

from game_data import GameData
from message_factory import MessageFactory


class GameWindow(tk.Tk, Observer):

    def __init__(self, message_factory: MessageFactory, game_data: GameData) -> None:
        super().__init__()
        self.message_factory: MessageFactory = message_factory
        game_data.register(self)

        self.lobby: tk.Toplevel = Lobby(self, message_factory, game_data)

        self.game_board: GameBoard = GameBoard(self)
        self.right_menu: RightMenu = RightMenu(self)
        self.left_menu: LeftMenu = LeftMenu(self)
        game_data.register(self.left_menu)

        self.left_menu.pack(side="left", fill="y")
        self.game_board.pack(side="left", fill="both", expand=True)
        self.right_menu.pack(side="right", fill="y")
        self.withdraw()

    def update_value(self, section, item, attribute, value):
        pass

