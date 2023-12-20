import tkinter as tk
import tkinter.ttk as ttk
import typing

from twisted.internet import reactor

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
            self.master: Lobby = lobby
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
            """ Structure of the data is similar to the structure in the GameData class """

        def __getitem__(self, item):
            return self._game_data[item]

        def __contains__(self, item: typing.Iterable) -> bool:
            """
            Expects a tuple (or other iterable object) with keys in the order (section, item, [attribute])
            :param item: tuple of keys
            :type item: Iterable
            :return: The given key exists
            :rtype: bool
            """
            if isinstance(item, typing.Iterable):
                try:
                    value = self
                    for i in item:
                        value = value[i]
                except (IndexError, KeyError):
                    return False
                return True
            return False

        def select(self, keys: typing.Iterable) -> tk.IntVar | tk.StringVar | tk.BooleanVar:
            """
            Returns a tkinter variable by keys. Keys are in an iterable in the order of (section, item, [attribute]).
            If the key is not present, raises an exception.
            :param keys: keys in the order of (section, item, [attribute])
            :type keys: Iterable
            :return: Tkinter variable
            :rtype: tk.IntVar | tk.StringVar | tk.BooleanVar
            """
            item = self
            for key in keys:
                item = item[key]
            return item

        def update(self, *, section: str, item: str | int, attribute: str | None = None, value: typing.Any) -> None:
            """
            Updates a value of a variable specified by the method attributes.
            :param section: Section is one of ("fields", "players", "misc")
            :type section: str
            :param item:
            :type item: str | int
            :param attribute: With section == "misc" the attribute = None
            :type attribute: str | None
            :param value: Value that will be stored into the variable
            :type value: Any
            """
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
        """ Class contains tkinter variables for this window. """
        self.game_data: GameData = game_data
        """ Link to game data """
        self.game_data.register(self)
        self.message_factory = message_factory
        """ Link to a message factory """
        self.tokens_list: list = config.available_tokens
        """ List of available tokens """
        self.table: ttk.Frame = ttk.Frame(self)
        """ Table containing all the elements """
        self.table_elements: list[typing.Any] = self._fill_table_elements()
        """ List of table elements, such as name fields, token comboboxes, etc. """
        self.buttons_frame: ttk.Frame = ttk.Frame(self)
        """  Frame containing buttons """
        self.buttons: list[typing.Any] = self._get_buttons()
        self.table.pack()
        self.buttons_frame.pack()
        self.protocol("WM_DELETE_WINDOW", self._close_window)

    def destroy(self):
        self.game_data.unregister(self)
        super().destroy()

    def update_value(self, *, section: str, item: str | int, attribute: str | None = None, value: typing.Any) -> None:
        """
        Updates a value of a variable specified by the method attributes.
        :param section: Section is one of ("fields", "players", "misc")
        :type section: str
        :param item:
        :type item: str | int
        :param attribute: With section == "misc" the attribute = None
        :type attribute: str | None
        :param value: Value that will be stored into the variable
        :type value: Any
        """
        if (section, item, value) == ("misc", "state", "pregame"):
            self.deiconify()
        if (section, item) == ("misc", "state") and value != "pregame":
            self.destroy()
        self.data.update(section=section, item=item, attribute=attribute, value=value)

    def set_my_player_id(self) -> None:
        """
        This method is called automatically when the player_id value is available. It causes that only the widgets
        of the player are changeable and adds tracing for the changes.
        """
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

    def _close_window(self) -> None:
        """
        Ends the entire app when this window is closed.
        """
        self.master.destroy()
        # noinspection PyUnresolvedReferences
        reactor.stop()

    def _fill_table_elements(self) -> list[list[tk.Widget]]:
        """
        Returns a table with tkinter elements. These elements master is self.table frame.
        :return: list[list]
        :rtype: Widget
        """
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

    def _get_buttons(self) -> list[tk.Widget]:
        """
        Returns a list with buttons. The master for the buttons is self.buttons_frame
        :return: list of buttons
        :rtype: list[Widget]
        """
        self.buttons_frame.configure(borderwidth=5)
        start_btn = ttk.Button(
            self.buttons_frame, text="Start Game", command=lambda: self.message_factory.send("start_game")
        )
        buttons = [start_btn]
        start_btn.pack()
        return buttons

    # noinspection PyUnusedLocal
    def _notify(self, name: str, something: str, mode: str) -> None:
        """
        Sends a message to the server when the value of a tkinter variable specified by the name attribute changes.
        :param name: The name of a tkinter variable
        :type name: str
        :param something: Mandatory attribute. It's not used by this method
        :type something: str
        :param mode: Mandatory attribute. It's not used by this method
        :type mode: str
        """
        keys: list[str | int] = name.split(".")
        keys[1] = int(keys[1])
        value = self.data.select(keys).get()
        self.message_factory.send(
            "user_info",
            {"section": keys[0], "item": keys[1], "attribute": keys[2], "value": value}
        )
