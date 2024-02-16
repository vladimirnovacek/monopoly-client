import itertools
import tkinter as tk
import typing
from tkinter import ttk

from interfaces import Updatable, Conditions

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class PlayerFrame(ttk.Frame):
    def __init__(self, master, player_id: int, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.player_id: int = player_id
        self.root: GameWindow = self.winfo_toplevel()
        self.name = ttk.Entry(self, justify=tk.CENTER)
        self.name.insert(0, f"Player {player_id + 1}")
        self.name.configure(state="disabled")
        self.cash = ttk.Label(self, text="0", anchor="center")
        self.left_arrow = ttk.Button(
            self,
            image=self.root.images["left_arrow"],
            command=self.left_arrow_click,
            style="Flat.TButton",
        )
        self.selected_token: int | None = None
        self.token = ttk.Label(self, image=self.root.not_selected_token, anchor="center")
        ttk.Style().configure("Flat.TButton", padding=0, relief="flat")
        self.right_arrow = ttk.Button(
            self,
            image=self.root.images["right_arrow"],
            command=self.right_arrow_click,
            style="Flat.TButton",
        )

    def draw(self, arrows: bool = True):
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        if self.player_id == self.root.game_data.get_id():
            self.name.configure(state="normal")
        self.name.grid(row=0, column=0, columnspan=3, sticky="news")
        self.cash.grid(row=1, column=0, columnspan=3, sticky="news")
        self.token.grid(row=2, column=1, sticky="news")
        if arrows:
            self.left_arrow.grid(row=2, column=0)
            self.right_arrow.grid(row=2, column=2)

    def hide_arrows(self):
        self.left_arrow.grid_remove()
        self.right_arrow.grid_remove()

    def left_arrow_click(self):
        if self.selected_token is None:
            self.selected_token = len(self.root.tokens) - 1
        else:
            self.selected_token -= 1
            if self.selected_token < 0:
                self.selected_token = len(self.root.tokens) - 1
        self.token.configure(image=self.root.tokens[self.selected_token])
        self.root.messenger.send(
            action="update_player",
            parameters={
                "attribute": "token",
                "value": os.path.splitext(os.path.basename(config.tokens[self.selected_token]))[0]},
        )

    def right_arrow_click(self):
        if self.selected_token is None:
            self.selected_token = 0
        else:
            self.selected_token += 1
            if self.selected_token >= len(self.winfo_toplevel().tokens):
                self.selected_token = 0
        self.token.configure(image=self.winfo_toplevel().tokens[self.selected_token])
        self.root.messenger.send(
            action="update_player",
            parameters={
                "attribute": "token",
                "value": os.path.splitext(os.path.basename(config.tokens[self.selected_token]))[0]},
        )


class PlayersFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.players: list[list[PlayerFrame]] = [[], []]
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        for i in range(2):
            for j in range(2):
                frame = PlayerFrame(self, i * 2 + j)
                frame.grid_propagate(tk.NO)
                self.players[i].append(frame)
                frame.grid(row=i, column=j, sticky="news")



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


