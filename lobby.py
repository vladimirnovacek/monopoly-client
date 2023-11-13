import tkinter as tk
import tkinter.ttk as ttk
import typing

import config
from game_data import GameData


class Lobby(tk.Tk):
    """
    Tkinter window lobby. Shows connected players and allows to player to change
    their name and token. When all players check the Ready checkbox, game can
    be started.

    For updating data in window by a GameData instance, call
    instance.register(lobby.game_data)
    """

    class GameData:
        """
        Class that holds tkinter variables used for this window.
        """

        def __init__(self, lobby):
            self.master = lobby
            self._game_data = {
                "players": [
                    {
                        "player_id": tk.IntVar(lobby, i),
                        "name": tk.StringVar(lobby, ""),
                        "token": tk.StringVar(lobby, ""),
                        "ready": tk.BooleanVar(lobby, False)
                    } for i in range(4)
                ],
                "misc": {
                    "my_id": tk.IntVar(lobby, -1),
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
                except (ValueError, KeyError):
                    return False
                return True
            try:
                if isinstance(item, typing.Iterable):
                    value = self
                    for i in item:
                        value = self[i]
                else:
                    self.__getitem__(item)
            except (ValueError, KeyError):
                return False
            return True

        def select(self, keys: typing.Iterable):
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
            self.select(keys).set(value)
            if section == "misc" and item == "my_id":
                self.master.set_my_player_id()

    def __init__(self):
        super().__init__()
        self.game_data: GameData = self.GameData(self)
        self.tokens_list: list = config.available_tokens
        """ List of available tokens """
        self.table: tk.Frame = tk.Frame(self)
        """ Table containing all the elements """
        self.table_elements: list[typing.Any] = self._fill_table_elements()
        """ List of table elements, such as name fields, token comboboxes, etc. """
        self.buttons: tk.Frame = tk.Frame(self)
        """  Frame containing buttons """  # TODO buttons not implemented
        self.table.pack()
        self.buttons.pack()

    def set_my_player_id(self):
        my_id = self.game_data["misc"]["my_id"].get()
        if my_id == -1:
            print("My_id is not set yet.")
            return
        self.table_elements[my_id][0].configure(state=tk.NORMAL)
        self.table_elements[my_id][1].configure(state="readonly")
        self.table_elements[my_id][2].configure(state=tk.NORMAL)

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

            player_data = self.game_data["players"][i]

            # Name textbox
            name_entry = tk.Entry(self.table, width=24, state=tk.DISABLED)
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
