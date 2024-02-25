import tkinter as tk
import typing
from tkinter import ttk

import config

from interfaces import Updatable

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class PlayerFrame(ttk.Frame):
    def __init__(self, master, player_id: int, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.root: GameWindow = self.winfo_toplevel()
        self.player_id: int = player_id

        self.root.style.configure("Flat.TButton", padding=0, relief="flat")
        self.root.style.configure("TEntry", padding=0, relief="flat", borderwidth=0)
        self.root.style.map(
            "TEntry",
            borderwidth=[("disabled", 0), ("!disabled", 0)],
            foreground=[("disabled", "black"), ("!disabled", "black")],
        )
        self.root.style.map(
            "Ready.TEntry",
            fieldbackground=[("disabled", "green1"), ("!disabled", "green1")],
        )
        self.root.style.map(
            "NotReady.TEntry",
            fieldbackground=[("disabled", "grey85"), ("!disabled", "white")],
        )
        self.root.style.map(
            "Highlighted.TEntry",
            fieldbackground=[("disabled", "beige"), ("!disabled", "beige")],
        )
        self.root.style.map(
            "NotHighlighted.TEntry",
            fieldbackground=[("disabled", "white"), ("!disabled", "white")],
        )

        self.name_value = f"Player {player_id + 1}"
        self.name = ttk.Entry(self, justify=tk.CENTER, style="NotReady.TEntry")
        self.name.insert(0, self.name_value)
        self.name.configure(state="disabled")
        self.name.bind("<Return>", lambda event: self.name_updated(event.widget.get()))
        self.name.bind("<KP_Enter>", lambda event: self.name_updated(event.widget.get()))
        self.name.bind("<FocusOut>", lambda event: self.name_updated(event.widget.get()))

        self.cash = ttk.Label(self, text="0", anchor="center")

        self.left_arrow = ttk.Button(
            self,
            image=self.root.images["left_arrow"],
            command=self.left_arrow_click,
            style="Flat.TButton",
        )

        self.selected_token_id: int  = -1
        self.token = ttk.Label(self, image=self.root.not_selected_token, anchor="center")

        self.right_arrow = ttk.Button(
            self,
            image=self.root.images["right_arrow"],
            command=self.right_arrow_click,
            style="Flat.TButton",
        )

    def draw(self, show_arrows: bool = True):
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        for attribute in ("name", "token", "ready"):
            if attribute in self.root.game_data.players[self.player_id]:
                self.update_player(attribute, self.root.game_data.players[self.player_id][attribute])
        if self.player_id == self.root.game_data.get_id():
            self.name.configure(state="normal")
            if show_arrows:
                self.left_arrow.grid(row=2, column=0)
                self.right_arrow.grid(row=2, column=2)
        self.name.grid(row=0, column=0, columnspan=3, sticky="news")
        self.cash.grid(row=1, column=0, columnspan=3, sticky="news")
        self.token.grid(row=2, column=1, sticky="news")

    def update_player(self, attribute: str, value: typing.Any):
        match attribute:
            case "ready":
                self.name.configure(style="Ready.TEntry" if value is True else "NotReady.TEntry")
            case "name":
                if value != self.name.get():
                    disable = False
                    if "disabled" in self.name.state():
                        self.name.configure(state="normal")
                        disable = True
                    self.name.delete(0, tk.END)
                    self.name.insert(0, value)
                    if disable:
                        self.name.configure(state="disabled")
            case "token":
                if value == "":
                    self.token.configure(image=self.root.not_selected_token)
                elif self.selected_token_id == -1 or value != config.tokens[self.selected_token_id]:
                    self.token.configure(image=self.root.tokens[config.tokens.index(value)])


    def destroy_arrows(self):
        self.left_arrow.destroy()
        self.right_arrow.destroy()

    def name_updated(self, name: str):
        if name != self.name_value:
            self.name_value = name
            self.root.right_menu.set_ready(False)
            self.root.messenger.send(
                action="update_player",
                parameters={
                    "attribute": "name",
                    "value": name
                }
            )

    def left_arrow_click(self):
        if self.selected_token_id is None:
            self.selected_token_id = len(self.root.tokens) - 1
        else:
            self.selected_token_id -= 1
            if self.selected_token_id < 0:
                self.selected_token_id = len(self.root.tokens) - 1
        self._set_token()

    def right_arrow_click(self):
        if self.selected_token_id is None:
            self.selected_token_id = 0
        else:
            self.selected_token_id += 1
            if self.selected_token_id >= len(self.root.tokens):
                self.selected_token_id = 0
        self._set_token()

    def start_game(self) -> None:
        if self.player_id == self.root.game_data.misc["on_turn"]:
            self.name.configure(style="Highlighted.TEntry")
        else:
            self.name.configure(style="NotHighlighted.TEntry")

    def set_control_states(self) -> None:
        if "update_player" in self.root.game_data.misc["possible_actions"]:
            self.name.configure(state="normal")
        else:
            self.name.configure(state="disabled")
            self.destroy_arrows()

    def _set_token(self):
        self.token.configure(image=self.root.tokens[self.selected_token_id])
        self.root.right_menu.set_ready(False)
        self.root.messenger.send(
            action="update_player",
            parameters={
                "attribute": "token",
                "value": config.tokens[self.selected_token_id]
            },
        )


class PlayersFrame(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.root: GameWindow = self.winfo_toplevel()
        self.players: list[PlayerFrame] = []
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        for i in range(4):
            frame = PlayerFrame(self, i)
            frame.grid_propagate(tk.NO)
            self.players.append(frame)
            frame.grid(row=i // 2, column=i % 2, sticky="news")

    def add_player(self, player_id: int):
        self.players[player_id].draw()

    def update_player(self, player_id, attribute, value) -> None:
        self.players[player_id].update_player(attribute, value)

    def start_game(self):
        self.sort_players()
        for frame in self.players:
            frame.start_game()

    def sort_players(self):
        for order, player_id in enumerate(self.root.game_data.misc["player_order"]):
            self.players[player_id].grid(row=order // 2, column=order % 2, sticky="news")

    def set_control_states(self):
        for frame in self.players:
            frame.set_control_states()

class RightMenu(ttk.Frame, Updatable):

    def __init__(self, master: "GameWindow", *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.root: GameWindow = master
        self.configure(relief="solid", borderwidth=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frm_players: PlayersFrame = PlayersFrame(self)
        self.frm_players.grid(row=0, column=0, sticky="news")

        self.frm_game_log = ttk.Frame(self)
        self.frm_game_log.grid(row=1, column=0, sticky="news")

        self.txt_game_log = tk.Text(self.frm_game_log, state=tk.DISABLED, width=40, height=12)
        self.txt_game_log.pack(expand=True, fill="both")

        self.frm_buttons = ttk.Frame(self)
        self.frm_buttons.grid(row=2, column=0, padx=10, pady=10, sticky="news")

        self.ready_state = "!selected"
        self.chk_ready = ttk.Checkbutton(self.frm_buttons, text="Ready", command=self._chk_ready_clicked)
        self.chk_ready.state(['!alternate', self.ready_state])
        self.chk_ready.pack(side=tk.LEFT)

        self.btn_end_turn = ttk.Button(self.frm_buttons, text="End turn")
        self.btn_end_turn.pack(side=tk.RIGHT)

    def add_player(self, player_id: int):
        self.frm_players.add_player(player_id)

    def update_player(self, player_id, attribute, value):
        self.frm_players.update_player(player_id, attribute, value)

    def start_game(self):
        self.chk_ready.destroy()
        self.frm_players.start_game()

    def set_ready(self, ready: bool) -> None:
        if ready != (self.ready_state == "selected"):
            self.chk_ready.state(["selected" if ready else "!selected"])
            self._chk_ready_clicked()

    def set_control_states(self):
        self.frm_players.set_control_states()
        if "update_player" in self.root.game_data.misc["possible_actions"]:
            self.chk_ready.pack(side=tk.LEFT)
        else:
            self.chk_ready.pack_forget()
        if "end_turn" in self.root.game_data.misc["possible_actions"]:
            self.btn_end_turn.configure(state=tk.NORMAL)
        else:
            self.btn_end_turn.configure(state=tk.DISABLED)

    def _chk_ready_clicked(self):
        if self.chk_ready.instate(['selected']):
            self.ready_state = "selected"
        else:
            self.ready_state = "!selected"
        self.root.messenger.send(
            action="update_player",
            parameters={
                "attribute": "ready",
                "value": self.ready_state == "selected"
            }
        )
