
import os.path
import random
import typing
from tkinter import BooleanVar

from PIL import ImageTk, Image

import config
from interfaces import Updatable

if typing.TYPE_CHECKING:
    from gameboard import GameBoard


class Dice(Updatable):

    class Die:
        images: list[ImageTk.PhotoImage]

        def __init__(self, master: "GameBoard", location: tuple[int, int]) -> None:
            self.master: GameBoard = master
            self.canvas_id = -1
            self.location = location
            self.animation_over = True
            self.animation_over_var = BooleanVar()
            self.displayed_value = 6

        def draw(self) -> None:
            if self.canvas_id == -1:
                self.canvas_id = self.master.create_image(
                    *self.location,
                    image=self.images[self.displayed_value - 1],
                    tags="dice",
                )

        def display_value(self, value: int) -> None:
            self.master.itemconfigure(
                self.canvas_id, image=self.images[value - 1])
            self.displayed_value = value

        def animate(self, value: int, iteration: int = 0, number_of_rotations: int = 0) -> None:
            """
             Provede animaci hodu kostkou. Výsledek hodu je předem dán v
            parametru value. Parametry iteration a number_of_rotations se při
            volání nezadávají.

            :param value: Hodnota, která se zobrazí na konci animace
            :param iteration: Počet dosud proběhlých iterací animace.
             Při volání se nezadává!
            :param number_of_rotations: Celkový počet otočení strany kostky.
             Při volání se nezadává!


            """
            self.animation_over = False

            def get_random_number() -> int:
                rnd = random.randint(1, 6)
                return rnd if rnd != self.displayed_value else \
                    get_random_number()
            delay, rotations_min, rotations_max = 100, 15, 30
            if number_of_rotations == 0:
                number_of_rotations = random.randint(
                    rotations_min, rotations_max)
            number_to_display = get_random_number()
            if iteration < number_of_rotations:
                self.display_value(number_to_display)
                self.master.after(
                    delay,
                    lambda: self.animate(
                        value, iteration + 1, number_of_rotations))
            else:
                self.display_value(value)
                self.animation_over = True
                self.animation_over_var.set(True)


    def __init__(self, master: "GameBoard") -> None:
        self.Die.images = [
            ImageTk.PhotoImage(
                Image.open(os.path.join(config.path_images, "dice", f"dice_{i}.png"))
            ) for i in range(1, 7)
        ]
        self.dice = [self.Die(master, location) for location in config.dice_location]
        self._animation_over_trace()
        self.animation_over_var = BooleanVar()

    def _animation_over_trace(self):
        for die in self.dice:
            die.animation_over_var.trace_add("write", self._animation_over_callback)

    def _animation_over_callback(self, *args):
        if all(die.animation_over_var.get() for die in self.dice):
            self.animation_over_var.set(True)
            for die in self.dice:
                die.animation_over_var.set(False)

    @property
    def animation_over(self):
        return all(die.animation_over for die in self.dice)

    def draw(self) -> None:
        for die in self.dice:
            die.draw()

    def display_values(self, values: tuple[int, int]):
        for i, die in zip(values, self.dice):
            die.display_value(i)

    def roll(self, values: tuple[int, int]):
        for i, die in zip(values, self.dice):
            die.animate(i)

    def update_value(self, section, item, attribute, value):
        if (section, item) == ("event", "dice_roll"):
            self.roll(value)