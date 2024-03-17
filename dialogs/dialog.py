import time
import tkinter as tk
import typing
from abc import ABC, abstractmethod

from dialogs.card import ChanceCcCard, StreetCard, UtilityCard, RailroadCard
from game_data import Field

if typing.TYPE_CHECKING:
    from game_window import GameWindow


class Dialog(tk.Canvas, ABC):
    @abstractmethod
    def show(self):
        raise NotImplementedError


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
        self.root = self.winfo_toplevel()
        self.card = ChanceCcCard(self)
        self.data = {"deck": deck, "id": card_id, "text": text}
        self.width, self.height = self.card.dimensions
        self.configure(width=self.width, height=self.height)

    def show(self):
        destroy = False
        def set_destroy():
            nonlocal destroy
            destroy = True
            self.update()
        self.card.show_card(self.data)
        self.bind("<Button-1>", lambda event: set_destroy())
        self.update()
        while not destroy:
            self.update()
        self.destroy()


class BuyDialog(Dialog):
    def __init__(self, master, field: Field, options: tuple[str] = ("buy", "auction")):
        super().__init__(master)
        self.root: GameWindow = self.winfo_toplevel()
        self.field = field
        if self.field["type"] == "street":
            self.card = StreetCard(self)
        elif self.field["type"] == "utility":
            self.card = UtilityCard(self)
        elif self.field["type"] == "railroad":
            self.card = RailroadCard(self)
        self.width = self.card.dimensions[0] * (1 + len(options) / 2)
        self.height = self.card.dimensions[1]
        self.card.x = self.width // 4 if "buy" in options else 0
        self.configure(width=self.width, height=self.height)
        self.options = options

    def show(self):
        self.card.show_card(self.field)
        if self.options:
            self.show_options()

    def show_options(self):
        if "buy" in self.options:
            self.create_rectangle(0, 0, self.width // 4, self.height, fill="green1", tags="buy")
            self.create_text(
                self.width // 8, self.height // 2,
                angle=90, text="Buy", anchor=tk.CENTER, font=self.card.font["title"], tags="buy"
            )
            self.tag_bind("buy", "<Button-1>", self._buy)
        if "auction" in self.options:
            self.create_rectangle(self.width * 3 // 4, 0, self.width, self.height, fill="red2", tags="auction")
            self.create_text(
                self.width * 7 // 8, self.height // 2,
                angle=270, text="Auction", anchor=tk.CENTER, font=self.card.font["title"], tags="auction"
            )
            self.tag_bind("auction", "<Button-1>", self._auction)

    def show_sold(self):
        self.card.sold()
        self.update()
        time.sleep(2)

    def _buy(self, *args):
        self.root.messenger.send("buy")

    def _auction(self, *args):
        self.root.messenger.send("auction")
