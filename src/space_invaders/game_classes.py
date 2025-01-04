import tkinter as tk
from structs import *


class Player:
    def __init__(self, image_src: str, rectangle: Rectangle):
        self.image = tk.PhotoImage(file=image_src)
        self.rectangle = rectangle

    def move_player(self, direction):
        print(self.rectangle)
        self.rectangle.x1 += (5 * direction)
        self.rectangle.x2 += (5 * direction)
        if self.rectangle.x1 > 570 or self.rectangle.x1 < 0:
            self.rectangle.x1 -= (5 * direction)
            self.rectangle.x2 -= (5 * direction)

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)


class Bullet:
    def __init__(self, image_src: str, rectangle: Rectangle):
        self.image = tk.PhotoImage(file=image_src)
        self.rectangle = rectangle

    def update(self):
        self.rectangle.y1 -= 5
        self.rectangle.y2 -= 5

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)


class Meteorite:
    def __init__(self, image_src: str, rectangle: Rectangle):
        self.image = tk.PhotoImage(file=image_src)
        self.rectangle = rectangle

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)