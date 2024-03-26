import time
import tkinter as tk
from typing import TYPE_CHECKING, Self
from abc import ABC
from tkinter import ttk
from typing import Literal

from dialogs.card import ChanceCcCard, StreetCard, UtilityCard, RailroadCard
from game_data import Field
from mixins import DragDropMixin

if TYPE_CHECKING:
    from game_window import GameWindow


def name2text(name: str) -> str:
    return name.translate(str.maketrans('_-', '  ')).capitalize()


class Dialog(DragDropMixin, tk.Canvas, ABC):
    def __init__(self, master: tk.Misc):
        super().__init__(master)
        self.root: GameWindow = self.winfo_toplevel()
        self.button_height = 30


class CardDialog(Dialog):
    """ Dialog displaying a Chance or Community Chest card. """
    def __init__(self, master: tk.Misc, deck: Literal["chance", "cc"], card_id: int, text: str):
        """
        :param master:
        :type master:
        :param deck:
        :type deck:
        :param card_id:
        :type card_id:
        :param text:
        :type text:
        """
        super().__init__(master)
        self.card = ChanceCcCard(self)
        self.data = {"deck": deck, "id": card_id, "text": text}
        self.width, self.height = self.card.dimensions
        self.configure(width=self.width, height=self.height)
        self.card.show_card(self.data)
        self.bind("<Button-3>", lambda event: self.destroy())


class DeedDialog(Dialog):
    @classmethod
    def get_buy_dialog(cls, master, field: Field) -> Self:
        return cls(master, field, buttons=('buy', 'auction'))

    @classmethod
    def get_overview_dialog(cls, master, field: Field) -> Self:
        if field['owner'] == master.root.game_data.my_id:
            if field['mortgage']:
                buttons = ('unmortgage', 'buy_houses')
            else:
                buttons = ('mortgage', 'buy_houses')
            return cls(master, field, buttons=buttons)
        return cls(master, field)

    def __init__(self, master, field: Field, **kwargs):
        super().__init__(master)
        self.field = field
        if self.field["type"] == "street":
            self.card = StreetCard(self)
        elif self.field["type"] == "utility":
            self.card = UtilityCard(self)
        elif self.field["type"] == "railroad":
            self.card = RailroadCard(self)
        self.width = self.card.dimensions[0]
        self.height = self.card.dimensions[1]
        self.configure(width=self.width, height=self.height)
        self.card.show_card(self.field)
        if 'buttons' in kwargs:
            self.show_options(kwargs['buttons'])

    def show_options(self, buttons: tuple | list):
        y = self.height
        self.height += self.button_height
        self.configure(height=self.height)
        button_width = self.width / len(buttons)
        for i, option in enumerate(buttons):
            x = button_width * i
            self.create_rectangle(x, y, x + button_width, self.height, fill="white", tags=option)
            self.create_text(
                x + button_width // 2, (self.height + y) // 2,
                text=name2text(option), anchor=tk.CENTER, tags=option, font=self.card.font['title']
            )
            self.tag_bind(option, "<Button-1>", lambda event, opt=option: getattr(self, f'_{opt}')())

    def show_sold(self):
        self.card.sold()
        self.update()
        time.sleep(2)

    def _buy(self):
        self.root.messenger.send("buy")

    def _auction(self):
        self.root.messenger.send("auction")

    def _mortgage(self):
        self.root.messenger.send('mortgage', {'field': self.field['field_id']})

    def _unmortgage(self):
        self.root.messenger.send('unmortgage', {'field': self.field['field_id']})

    def _buy_houses(self):
        pass


class PropertyListDialog(Dialog):
    def __init__(self, master: tk.Misc, player_id: int = -1):
        super().__init__(master)
        if player_id == -1:
            player_id = self.root.game_data.my_id
        owned_properties = [
            field for field in self.root.game_data.fields.values()
            if field.get('owner', None) == player_id
        ]
        names = [field['name'] for field in owned_properties]
        cbx_names = tk.Listbox(self, selectmode=tk.SINGLE, exportselection=False)
        cbx_names.insert(tk.END, *names)
        cbx_names.pack()
        if player_id == self.root.game_data.my_id:
            self.btn_mortgage = ttk.Button(self, image=self.root.images["mortgage"], command=self._mortgage)
            self.btn_mortgage.pack()

    def show(self):
        pass

    def _mortgage(self):
        pass