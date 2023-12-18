import tkinter as tk
import tkinter.ttk as ttk
import typing

import config
from game_data import GameData
from interfaces import Observer
from message_factory import MessageFactory


class Lobby(tk.Toplevel, Observer):
    """
    Tkinter window lobby. Shows connected players and allows to player to change
    their name and token. When all players check the Ready checkbox, game can
    be started.

    For updating data in window by a GameData instance, call
    instance.register(lobby.game_data)
    """

    class Data:
        """
        Class that holds tkinter variables used for this window.
        """

        def __init__(self, lobby):
            self.master = lobby
            self._game_data = {
                "players": [
                    {
                        "player_id": tk.IntVar(lobby, i, name=f"players.{i}.player_id"),
                        "name": tk.StringVar(lobby, "", name=f"players.{i}.name"),
                        "token": tk.StringVar(lobby, "", name=f"players.{i}.token"),
                        "ready": tk.BooleanVar(lobby, False, name=f"players.{i}.ready")
                    } for i in range(4)
                ],
                "misc": {
                    "my_id": tk.IntVar(lobby, -1, name=f"misc.my_id"),
                }
            }

        def __getitem__(self, item):
            return self._game_data[item]

        def __contains__(self, item):
            if isinstance(item, typing.Iterable):
                try:
                    value = self
                    for i in item:
                        value = value[i]
                except (IndexError, KeyError):
                    return False
                return True
            try:
                if isinstance(item, typing.Iterable):
                    _ = self
                    for i in item:
                        _ = self[i]
                else:
                    self.__getitem__(item)
            except (ValueError, KeyError):
                return False
            return True

        def select(self, keys: typing.Iterable) -> tk.IntVar | tk.StringVar | tk.BooleanVar:
            item = self
            for key in keys:
                item = item[key]
            return item

        def update(self, *, section, item, attribute=None, value):
            if attribute:
                keys = (section, item, attribute)
            else:
                keys = (section, item)
            if keys not in self:
                return
            if self.select(keys).get() != value:
                self.select(keys).set(value)
            if section == "misc" and item == "my_id":
                self.master.set_my_player_id()


    master: tk.Tk

    def __init__(self, master: tk.Tk, message_factory: MessageFactory, game_data: GameData):
        super().__init__(master=master)
        self.data: Lobby.Data = self.Data(self)
        self.game_data = game_data
        self.game_data.register(self)
        self.message_factory = message_factory
        self.tokens_list: list = config.available_tokens
        """ List of available tokens """
        self.table: ttk.Frame = ttk.Frame(self)
        """ Table containing all the elements """
        self.table_elements: list[typing.Any] = self._fill_table_elements()
        """ List of table elements, such as name fields, token comboboxes, etc. """
        self.buttons_frame: ttk.Frame = ttk.Frame(self)
        """  Frame containing buttons """  # TODO buttons not implemented
        self.buttons: list[typing.Any] = self._get_buttons()
        self.table.pack()
        self.buttons_frame.pack()

    def update_value(self, section, item, attribute, value):
        self.data.update(section=section, item=item, attribute=attribute, value=value)

    def set_my_player_id(self):
        my_id = self.data["misc"]["my_id"].get()
        if my_id == -1:
            print("My_id is not set yet.")
            return
        key = ["players", my_id]
        name_entry: tk.Entry = self.table_elements[my_id + 1][0]
        name_entry.configure(state=tk.NORMAL)
        name_entry.var = self.data.select(key + ["name"])
        name_entry.var.trace_add("write", self._notify)
        token_combobox: ttk.Combobox = self.table_elements[my_id + 1][1]
        token_combobox.configure(state="readonly")
        token_combobox.var = self.data.select(key + ["token"])
        token_combobox.var.trace_add("write", self._notify)
        ready_checkbox: ttk.Checkbutton = self.table_elements[my_id + 1][2]
        ready_checkbox.configure(state=tk.NORMAL)
        ready_checkbox.var = self.data.select(key + ["ready"])
        ready_checkbox.var.trace_add("write", self._notify)

    def _notify(self, name: str, something: str, mode: str):
        keys: list[str | int] = name.split(".")
        keys[1] = int(keys[1])
        value = self.data.select(keys).get()
        self.message_factory.send(
            "user_info",
            {"section": keys[0], "item": keys[1], "attribute": keys[2], "value": value}
        )

    def _fill_table_elements(self) -> list[list]:
        table_elements: list[list] = [[
            tk.Label(self.table, text='Name'),
            tk.Label(self.table, text='Token'),
            tk.Label(self.table, text="Ready")
        ]]  # Header of the table
        for i in range(3):
            table_elements[0][i].grid(column=i, row=0, padx=5, pady=5, sticky=tk.W)  # place headers to the grid

        for i in range(4):  # next lines are text entries a comboboxes
            table_elements.append(list())  # A line is represented with a list

            player_data = self.data["players"][i]

            # Name textbox
            name_entry = ttk.Entry(self.table, width=24, state=tk.DISABLED)
            name_entry.configure(textvariable=player_data["name"])

            # Token selection combobox
            token_list = ttk.Combobox(self.table, values=self.tokens_list, state=tk.DISABLED, width=16)

            token_list.configure(textvariable=player_data["token"])

            # Ready checkbox
            chbox = ttk.Checkbutton(self.table, state=tk.DISABLED)
            chbox.configure(variable=player_data["ready"])

            for j, v in enumerate((name_entry, token_list, chbox)):
                table_elements[i + 1].append(v)  # place element to the list
                table_elements[i + 1][j].grid(column=j, row=i + 1, padx=5, pady=5)  # Place element to the grid
        return table_elements

    def _get_buttons(self):
        self.buttons_frame.configure(borderwidth=5)
        start_btn = ttk.Button(self.buttons_frame, text="Start Game", command=self._start_game)
        buttons = [start_btn]
        start_btn.pack()
        return buttons

    def _start_game(self):
        self.master.deiconify()
        self.destroy()

