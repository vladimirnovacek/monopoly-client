
from __future__ import annotations

import tkinter as tk

from gameboard import GameBoard
from leftmenu import LeftMenu
from rightmenu import RightMenu

from game_data import GameData
from message_factory import MessageFactory


class GameWindow(tk.Tk):

    def __init__(self, message_factory: MessageFactory, game_gata: GameData) -> None:
        super().__init__()
        self.message_factory = message_factory
        game_gata.register(self)
        self.game_board: GameBoard = GameBoard(self)
        self.right_menu: RightMenu = RightMenu(self)
        self.left_menu: LeftMenu = LeftMenu(self)

        self.left_menu.pack(side="left", fill="y")
        self.game_board.pack(side="left", fill="both", expand=True)
        self.right_menu.pack(side="right", fill="y")

    def update(self):
        pass

