import itertools
import tkinter as tk
import typing
from tkinter import ttk

from interfaces import Updatable, Conditions

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class PlayersFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure()
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        for i in range(2):
            for j in range(2):
                label_text = f"Label {i * 2 + j + 1}"
                label = tk.Label(self, text=label_text, padx=10, pady=10)
                label.grid(row=i, column=j)



class RightMenu(ttk.Frame, Updatable):

    def __init__(self, master: "GameWindow", *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.configure(relief="solid", borderwidth=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frm_players: PlayersFrame = PlayersFrame(self)
        self.frm_players.grid(row=0, column=0, sticky="news")

        self.frm_game_log = ttk.Frame(self)
        self.frm_game_log.grid(row=1, column=0, sticky="news")

        self.txt_game_log = tk.Text(self.frm_game_log, state=tk.DISABLED, width=40, height=12)
        self.txt_game_log.pack(expand=True, fill="both")

        # self.frm_buttons = ttk.Frame(self)
        # self.frm_buttons.grid(row=2, column=0, padx=10, pady=10, sticky="news")

        self.btn_end_turn = ttk.Button(self, text="End turn", command=self.end_turn)
        self.btn_end_turn.grid(row=2, column=0, pady=20, sticky="e")

    def get_conditions(self) -> set[Conditions]:
        conditions = {
            Conditions(self.update_value, section="players", attribute="possible_actions")
        }
        conditions.update(super().get_conditions())
        return conditions

    def update_value(self, section, item, attribute, value):
        if section == "players" and attribute == "possible_actions":
            if self.master.game_data.on_turn:
                for name, button in self.buttons.items():
                    if name in value:
                        button.configure(state=tk.NORMAL)
                    else:
                        button.configure(state=tk.DISABLED)

    def process_actions(self, data: set[str]):
        for button_name, button in self.buttons.items():
            if button_name in data:
                button.configure(state=tk.NORMAL)
            else:
                button.configure(state=tk.DISABLED)


