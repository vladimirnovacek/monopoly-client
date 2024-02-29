import os
import time
from abc import ABC
from enum import Enum
import tkinter as tk
import tkinter.font as tkfont
from string import Template

import config
from game_data import Field


class Color(Enum):
    BROWN = "#784d3c"
    LBLUE = "#badaee"
    PURPLE = "#aa3b80"
    ORANGE = "#d58a37"
    RED = "#bb292c"
    YELLOW = "#fff139"
    GREEN = "#5fa55d"
    DBLUE = "#2c67a1"


class Card(ABC):

    def __init__(self, canvas: tk.Canvas, x: int = 0, y: int = 0):
        self.x: int = x
        self.y: int = y
        self._pos: dict = {}
        self._dim: dict = {}
        self.font = {
            "deed": tkfont.Font(size=6),
            "title": tkfont.Font(size=12, weight=tk.font.BOLD),
            "text": tkfont.Font(size=8),
            "text_2": tkfont.Font(size=7),
            "small": tkfont.Font(size=6),
            "sold": tkfont.Font(size=40, weight=tk.font.BOLD)
        }
        self.canvas: tk.Canvas = canvas
        self.card_data: dict = {}
        self.ids = {}
        self.tags = ["card"]

    @property
    def dimensions(self):
        x = max([pair[0] for pair in self._dim.values()])
        y = max([pair[1] for pair in self._dim.values()])
        return x, y

    @property
    def pos_dim(self):
        return {
            key: self._pos[key] + self._dim[key]
            for key in self._pos if key in self._dim
        }

    def show_card(self, data):
        self._set_info(data)
        self._show()

    def _set_info(self, data):
        ...

    def paint(self):
        ...

    def repaint(self):
        ...

    def add_all_tags(self, tag_or_id):
        for tag in self.tags:
            self.canvas.addtag_withtag(tag, tag_or_id)

    def add_tag_and_below(self, tag_or_id, tag):
        if tag not in self.tags:
            raise ValueError(f"Tag {tag} not in self.tags")
        index = self.tags.index(tag)
        for t in self.tags[:index + 1]:
            self.canvas.addtag_withtag(t, tag_or_id)

    def _show(self):
        if not self.ids:  # ještě nebylo vykresleno
            self.paint()
        else:
            self.repaint()

    def _hide(self, event: tk.Event):
        self.canvas.itemconfigure("card", state=tk.HIDDEN)

    def _position(self, x, y) -> tuple[int, int]:
        """
        Posune souřadnice podle souřadnic počátku objektu x, y
        :param x:
        :param y:
        :return: tuple[int, int]
        """
        x += self.x
        y += self.y
        return x, y

    def _dimensions(self, x, y, width, height) -> tuple[int, int, int, int]:
        """
        Převede rozměry z formátu x, y, šířka, výška do formátu x1, y1, x2, y2,
        kde x1, y1 jsou souřadnice levného horního rohu a x2, y2 pravého
        dolního. Zároveň je posune na souřadnice počátku objektu podle
        atributů třídy x, y.

        :param x:
        :param y:
        :param width:
        :param height:
        :return: tuple[int, int, int, int]
        """
        x1 = self.x + x
        y1 = self.y + y
        x2 = x1 + width
        y2 = y1 + height
        return x1, y1, x2, y2


class PropertyCard(Card):
    """ Abstraktní třída představující grafické znázornění karty ulice,
    železnice nebo utility.
    """
    TAG = "property_card"

    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas)
        self._pos |= {
            "card": (0, 0),
            "card_frame": (3, 3),
            "question": (110, -20),
            "yes": (167, 20),
            "no": (167, 55),
            "sold": (78, 120),
        }
        self._dim |= {
            "card": (157, 240),
            "card_frame": (151, 234)
        }
        self._text = {
            "sold": "Sold"
        }
        self._x0 = 0
        self._y0 = 0
        self.buy: tk.BooleanVar = tk.BooleanVar(self.canvas)
        self.tags.append("property_card")

    def rent_dialog(self, player_name: str, rent: str):
        self.ids["rent_text"] = self.canvas.create_text(
            self._position(*self._pos["question"]),
            text=f"This property is owned by {player_name}. You have to pay him"
                 f"£{rent}.",
            font=self.font["title"], width=250, justify=tk.CENTER
        )

    def buy_dialog(self):
        self.ids["buy_question"] = self.canvas.create_text(
            self._position(*self._pos["question"]),
            text=f"Do you want to buy this property for "
                 f"£{self.card_data['price']}?",
            font=self.font["title"], width=250, justify=tk.CENTER
        )
        btn_yes = tk.Button(self.canvas, text="Yes", command=self._yes_clicked)
        btn_no = tk.Button(self.canvas, text="No", command=self._no_clicked)
        self.ids["yes_answer"] = self.canvas.create_window(
            self._position(*self._pos["yes"]), window=btn_yes, anchor=tk.NW,
            width=60
        )
        self.ids["no_answer"] = self.canvas.create_window(
            self._position(*self._pos["no"]), window=btn_no, anchor=tk.NW,
            width=60
        )
        self.canvas.addtag_withtag("buy_dialog", self.ids["buy_question"])
        self.canvas.addtag_withtag("buy_dialog", self.ids["yes_answer"])
        self.canvas.addtag_withtag("buy_dialog", self.ids["no_answer"])
        self.add_tag_and_below("buy_dialog", PropertyCard.TAG)
        self.canvas.wait_variable(self.buy)
        if self.buy.get():
            self.sold()
        self.canvas.itemconfigure("buy_dialog", state=tk.HIDDEN)
        self.canvas.tag_bind(self.tags[0], "<Button-1>", self._hide)
        return self.buy.get()

    def sold(self) -> None:
        if "sold" in self.ids.keys():
            self.canvas.itemconfigure(self.ids["sold"], state=tk.NORMAL)
        else:
            # noinspection PyArgumentList
            self.ids["sold"] = self.canvas.create_text(
                self._position(*self._pos["sold"]),
                text=self._text["sold"].upper(), anchor=tk.CENTER,
                font=self.font["sold"], fill="red", angle=45,
            )
            self.add_tag_and_below(self.ids["sold"], PropertyCard.TAG)

    def _yes_clicked(self):
        self.buy.set(True)

    def _no_clicked(self):
        self.buy.set(False)

    def _show(self):
        if not self.ids:  # ještě nebylo vykresleno
            self.paint()
        else:
            self.repaint()

    def _hide(self, event: tk.Event):
        self.canvas.tag_unbind(self.tags[0], "<Button-1>")
        self.canvas.itemconfigure(self.tags[0], state=tk.HIDDEN)


class UtilityCard(PropertyCard):

    TAG = "utility_card"

    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas)
        self.tags.append(self.TAG)
        self.images: dict[str, tk.PhotoImage] = {
            "electric_company": tk.PhotoImage(file=os.path.join(
                config.path_cards, "electric_company.png"
            )),
            "water_works": tk.PhotoImage(file=os.path.join(
                config.path_cards, "water_works.png"
            )),
        }
        self._pos |= {
            "image": (78, 8),
            "name": (78, 92),
            "paragraph_1": (78, 130),
            "paragraph_2": (78, 180)
        }
        self._text |= {
            "paragraph_1": "If one Utility is owned, rent is 4 times amount "
                           "shown on dice.",
            "paragraph_2": "If both Utilities are owned, rent is 10 times "
                           "amount shown on dice."
        }

    def _set_info(self, data):
        necessary_keys = (
            "name", "price", "rent", "rent_2"
        )
        assert all(key in data for key in necessary_keys)
        self.card_data = data

    def _get_image(self):
        if self.card_data["index"] == "utility_1":
            image = "electric_company"
        elif self.card_data["index"] == "utility_2":
            image = "water_works"
        else:
            raise ValueError(f"Incorrect field index {self.card_data['index']}")
        return self.images[image]

    def paint(self):
        self.ids["card"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["card"]), fill="white"
        )
        self.ids["frame"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["card_frame"])
        )
        self.ids["image"] = self.canvas.create_image(
            self._position(*self._pos["image"]),
            image=self._get_image(), anchor=tk.N)
        self.ids["name"] = self.canvas.create_text(
            self._position(*self._pos["name"]), anchor=tk.N, justify=tk.CENTER,
            font=self.font["title"], text=self.card_data["name"].upper(),
            width=self._dim["card_frame"][0] - 6
        )
        self.ids["paragraph_1"] = self.canvas.create_text(
            self._position(*self._pos["paragraph_1"]), anchor=tk.N,
            text=self._text["paragraph_1"], font=self.font["text"],
            width=self._dim["card_frame"][0] - 6, justify=tk.CENTER
        )
        self.ids["paragraph_2"] = self.canvas.create_text(
            self._position(*self._pos["paragraph_2"]), anchor=tk.N,
            text=self._text["paragraph_2"], font=self.font["text"],
            width=self._dim["card_frame"][0] - 6, justify=tk.CENTER
        )
        for elem in self.ids.values():
            self.add_all_tags(elem)


class RailroadCard(PropertyCard):

    TAG = "railroad_card"

    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas)
        self.tags.append(self.TAG)
        self.images: dict[str, tk.PhotoImage] = {}
        self._pos |= {
            "image": (78, 8),
            "name": (78, 92),
            "rent_left": (6, 140),
            "rent_right": (151, 140),
            "rent_2_left": (6, 160),
            "rent_2_right": (151, 160),
            "rent_3_left": (6, 180),
            "rent_3_right": (151, 180),
            "rent_4_left": (6, 200),
            "rent_4_right": (151, 200)
        }
        self._text |= {
            "rent": "RENT",
            "rent_2": Template("If $n railroads are owned")
        }

    def _set_info(self, data):
        necessary_keys = (
            "name", "price", "rent", "rent_2", "rent_3", "rent_4"
        )
        assert all(key in data for key in necessary_keys)
        self.card_data = data

    def paint(self):
        self.images["train"] = tk.PhotoImage(file=os.path.join(
            config.path_cards, "train.png"
        ))
        self.ids["card"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["card"]), fill="white"
        )
        self.ids["frame"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["card_frame"])
        )
        self.ids["image"] = self.canvas.create_image(
            self._position(*self._pos["image"]),
            image=self.images["train"], anchor=tk.N)
        self.ids["name"] = self.canvas.create_text(
            self._position(*self._pos["name"]), anchor=tk.N, justify=tk.CENTER,
            font=self.font["title"], text=self.card_data["name"].upper(),
            width=self._dim["card_frame"][0] - 6
        )
        self.ids["rent_left"] = self.canvas.create_text(
            self._position(*self._pos["rent_left"]), anchor=tk.NW,
            font=self.font["text_2"], text=self._text["rent"]
        )
        self.ids["rent_right"] = self.canvas.create_text(
            self._position(*self._pos["rent_right"]), anchor=tk.NE,
            font=self.font["text_2"], text=f"£{self.card_data['rent']}"
        )
        self.ids["rent_2_left"] = self.canvas.create_text(
            self._position(*self._pos["rent_2_left"]), anchor=tk.NW,
            font=self.font["text_2"], text=self._text["rent_2"].substitute(n=2)
        )
        self.ids["rent_2_right"] = self.canvas.create_text(
            self._position(*self._pos["rent_2_right"]), anchor=tk.NE,
            font=self.font["text_2"], text=f"£{self.card_data['rent_2']}"
        )
        self.ids["rent_3_left"] = self.canvas.create_text(
            self._position(*self._pos["rent_3_left"]), anchor=tk.NW,
            font=self.font["text_2"], text=self._text["rent_2"].substitute(n=3)
        )
        self.ids["rent_3_right"] = self.canvas.create_text(
            self._position(*self._pos["rent_3_right"]), anchor=tk.NE,
            font=self.font["text_2"], text=f"£{self.card_data['rent_3']}"
        )
        self.ids["rent_4_left"] = self.canvas.create_text(
            self._position(*self._pos["rent_4_left"]), anchor=tk.NW,
            font=self.font["text_2"], text=self._text["rent_2"].substitute(n=4)
        )
        self.ids["rent_4_right"] = self.canvas.create_text(
            self._position(*self._pos["rent_4_right"]), anchor=tk.NE,
            font=self.font["text_2"], text=f"£{self.card_data['rent_4']}"
        )

        for elem in self.ids.values():
            self.add_all_tags(elem)

    def repaint(self):
        print(self.card_data)
        self.canvas.itemconfigure(
            self.ids["name"], text=self.card_data["name"].upper()
        )
        self.canvas.itemconfigure(
            self.ids["rent_right"], text=f"£{self.card_data['rent']}"
        )
        self.canvas.itemconfigure(
            self.ids["rent_2_right"], text=f"£{self.card_data['rent_2']}"
        )
        self.canvas.itemconfigure(
            self.ids["rent_3_right"], text=f"£{self.card_data['rent_3']}"
        )
        self.canvas.itemconfigure(
            self.ids["rent_4_right"], text=f"£{self.card_data['rent_4']}"
        )
        self.canvas.itemconfigure(self.TAG, state=tk.NORMAL)


class StreetCard(PropertyCard):

    TAG = "street_card"

    def __init__(self, canvas: tk.Canvas):
        super().__init__(canvas)
        self.tags.append(self.TAG)

        self._pos |= {
            "header": (3, 3),
            "line": (6, 177),
            "deed": (78, 6),
            "street_name": (78, 32),
            "rent_left": (6, 55),
            "rent_right": (151, 57),
            "rent_2_left": (6, 72),
            "rent_2_right": (151, 72),
            "house_1_left": (6, 89),
            "house_1_right": (151, 89),
            "houses_icon": (90, 87),
            "house_2_left": (6, 106),
            "house_2_right": (151, 106),
            "house_3_left": (6, 123),
            "house_3_right": (151, 123),
            "house_4_left": (6, 140),
            "house_4_right": (151, 140),
            "hotel_left": (6, 157),
            "hotel_right": (151, 157),
            "house_price_left": (6, 184),
            "house_price_right": (151, 184),
            "hotel_price_left": (6, 201),
            "hotel_price_right": (151, 201),
            "plus_houses": (151, 212)
        }
        self._dim |= {
            "header": (151, 48),
            "line": (145, 0)
        }
        self._text |= {
            "deed": "Title deed",
            "rent": "Rent",
            "double_rent": "Rent with color set",
            "house_rent": "Rent with",
            "house_price": "Houses cost",
            "hotel_price": "Hotels cost",
            "plus_houses": "(plus 4 houses)"
        }

        # noinspection PyUnresolvedReferences
        self.houses = tk.PhotoImage(
            file=os.path.join(config.path_cards, "houses.png")
        )

    def _set_info(self, data: dict):
        necessary_keys = (
            "name", "color", "rent", "double_rent", "house_1", "house_2",
            "house_3", "house_4", "hotel", "house_price", "hotel_price",
            "price"
        )
        assert all(key in data for key in necessary_keys)
        self.card_data = data

    # noinspection PyTypeChecker,PyArgumentList
    def paint(self):
        self.ids["card"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["card"]), fill="white"
        )
        self.ids["frame"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["card_frame"])
        )
        self.ids["header"] = self.canvas.create_rectangle(
            self._dimensions(*self.pos_dim["header"]),
            fill=Color[self.card_data["color"].upper()].value
        )
        self.ids["line"] = self.canvas.create_line(
            self._dimensions(*self.pos_dim["line"])
        )
        self.ids["deed"] = self.canvas.create_text(
            self._position(*self._pos["deed"]), anchor=tk.N, justify=tk.CENTER,
            text=self._text["deed"].upper(), font=self.font["deed"]
        )
        self.ids["street_name"] = self.canvas.create_text(
            self._position(*self._pos["street_name"]), anchor=tk.CENTER,
            justify=tk.CENTER, text=self.card_data["name"].upper(),
            font=self.font["title"], width=self._dim["card_frame"][0] - 6
        )
        self.ids["rent_left"] = self.canvas.create_text(
            self._position(*self._pos["rent_left"]), anchor=tk.NW,
            text=self._text["rent"], font=self.font["text"]
        )
        self.ids["rent_right"] = self.canvas.create_text(
            self._position(*self._pos["rent_right"]), anchor=tk.NE,
            text=f"£{self.card_data['rent']}", font=self.font["text"]
        )
        self.ids["rent_2_left"] = self.canvas.create_text(
            self._position(*self._pos["rent_2_left"]), anchor=tk.NW,
            text=self._text["double_rent"], font=self.font["text"]
        )
        self.ids["rent_2_right"] = self.canvas.create_text(
            self._position(*self._pos["rent_2_right"]), anchor=tk.NE,
            text=f"£{self.card_data['double_rent']}", font=self.font["text"]
        )
        settings_left = {
            "anchor": tk.NW, "text": self._text["house_rent"],
            "font": self.font["text"]
        }
        settings_right = {"anchor": tk.NE, "font": self.font["text"]}
        self.ids["house_1_left"] = self.canvas.create_text(
            self._position(*self._pos["house_1_left"]), settings_left
        )
        self.ids["house_1_right"] = self.canvas.create_text(
            self._position(*self._pos["house_1_right"]), settings_right,
            text=f"£{self.card_data['house_1']}"
        )
        self.ids["houses"] = self.canvas.create_image(
            self._position(*self._pos["houses_icon"]), anchor=tk.NW,
            image=self.houses
        )
        self.ids["house_2_left"] = self.canvas.create_text(
            self._position(*self._pos["house_2_left"]), settings_left
        )
        self.ids["house_2_right"] = self.canvas.create_text(
            self._position(*self._pos["house_2_right"]), settings_right,
            text=f"£{self.card_data['house_2']}"
        )
        self.ids["house_3_left"] = self.canvas.create_text(
            self._position(*self._pos["house_3_left"]), settings_left
        )
        self.ids["house_3_right"] = self.canvas.create_text(
            self._position(*self._pos["house_3_right"]), settings_right,
            text=f"£{self.card_data['house_3']}"
        )
        self.ids["house_4_left"] = self.canvas.create_text(
            self._position(*self._pos["house_4_left"]), settings_left
        )
        self.ids["house_4_right"] = self.canvas.create_text(
            self._position(*self._pos["house_4_right"]), settings_right,
            text=f"£{self.card_data['house_4']}"
        )
        self.ids["hotel_left"] = self.canvas.create_text(
            self._position(*self._pos["hotel_left"]), settings_left
        )
        self.ids["hotel_right"] = self.canvas.create_text(
            self._position(*self._pos["hotel_right"]), settings_right,
            text=f"£{self.card_data['hotel']}"
        )
        self.ids["house_price_left"] = self.canvas.create_text(
            self._position(*self._pos["house_price_left"]), anchor=tk.NW,
            text=self._text["house_price"], font=self.font["text"]
        )
        self.ids["house_price_right"] = self.canvas.create_text(
            self._position(*self._pos["house_price_right"]), anchor=tk.NE,
            text=f"£{self.card_data['house_price']} each",
            font=self.font["text"]
        )
        self.ids["hotel_price_left"] = self.canvas.create_text(
            self._position(*self._pos["hotel_price_left"]), anchor=tk.NW,
            text=self._text["hotel_price"], font=self.font["text"]
        )
        self.ids["hotel_price_right"] = self.canvas.create_text(
            self._position(*self._pos["hotel_price_right"]), anchor=tk.NE,
            text=f"£{self.card_data['hotel_price']} each",
            font=self.font["text"]
        )
        self.ids["plus_houses"] = self.canvas.create_text(
            self._position(*self._pos["plus_houses"]), anchor=tk.NE,
            text=self._text["plus_houses"], font=self.font["small"]
        )
        for elem in self.ids.values():
            for tag in self.tags:
                self.canvas.addtag_withtag(tag, elem)
            # self.canvas.addtag_withtag(
            #     f"{self.tags[-1]}_essential", elem)

    def repaint(self):
        self.canvas.itemconfigure(
            self.ids["header"],
            fill=Color[self.card_data["color"].upper()].value
        )
        self.canvas.itemconfigure(
            self.ids["street_name"], text=self.card_data["name"].upper()
        )
        self.canvas.itemconfigure(
            self.ids["rent_right"], text=f"£{self.card_data['rent']}"
        )
        self.canvas.itemconfigure(
            self.ids["rent_2_right"], text=f"£{self.card_data['double_rent']}"
        )
        self.canvas.itemconfigure(
            self.ids["house_1_right"], text=f"£{self.card_data['house_1']}"
        )
        self.canvas.itemconfigure(
            self.ids["house_2_right"], text=f"£{self.card_data['house_2']}"
        )
        self.canvas.itemconfigure(
            self.ids["house_3_right"], text=f"£{self.card_data['house_3']}"
        )
        self.canvas.itemconfigure(
            self.ids["house_4_right"], text=f"£{self.card_data['house_4']}"
        )
        self.canvas.itemconfigure(
            self.ids["hotel_right"], text=f"£{self.card_data['hotel']}"
        )
        self.canvas.itemconfigure(
            self.ids["house_price_right"],
            text=f"£{self.card_data['house_price']} each"
        )
        self.canvas.itemconfigure(
            self.ids["hotel_price_right"],
            text=f"£{self.card_data['hotel_price']} each"
        )
        self.canvas.itemconfigure("street_card", state=tk.NORMAL)


class BuyDialog(tk.Canvas):
    def __init__(self, master, field: Field, options: tuple[str] = ("buy", "auction")):
        super().__init__(master)
        self.root = self.winfo_toplevel()
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