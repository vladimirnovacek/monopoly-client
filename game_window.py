
from __future__ import annotations

import tkinter as tk

from interfaces import Updatable, Conditions, Observer
from gameboard import GameBoard
from leftmenu import LeftMenu
from lobby import Lobby
from rightmenu import RightMenu

from game_data import GameData
from message_factory import MessageFactory


class GameWindow(tk.Tk, Observer, Updatable):

    def __init__(self, message_factory: MessageFactory, game_data: GameData) -> None:
        super().__init__()
        self.message_factory: MessageFactory = message_factory
        self.game_data: GameData = game_data
        self.game_data.register(self)

        self.lobby: Lobby = Lobby(self, message_factory)

        self.game_board: GameBoard = GameBoard(self)
        self.right_menu: RightMenu = RightMenu(self)
        self.left_menu: LeftMenu = LeftMenu(self)

        self.left_menu.pack(side="left", fill="y")
        self.game_board.pack(side="left", fill="both", expand=True)
        self.right_menu.pack(side="right", fill="y")

        self.subclasses: set[Updatable] = {self.lobby, self.left_menu, self.game_board, self.right_menu}
        self._conditions = self.get_conditions()

    def get_conditions(self) -> set[Conditions]:
        conditions = {
            Conditions(self.deiconify, False, section="events", item="game_started"),
            Conditions(self.withdraw, False, section="misc", item="state", value="pregame"),
        }
        conditions.update(super().get_conditions())
        return conditions
        
    def update_value(self, section, item, attribute, value):
        for condition in self._conditions:
            condition.call(section=section, item=item, attribute=attribute, value=value)

    def destroy(self):
        self.game_data.unregister(self)
        super().destroy()