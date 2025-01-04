import tkinter as tk
from constructs import *


class Player:
    def __init__(self, image_src: str, position: Vector2, rectangle: Rectangle):
        self.player_img = tk.PhotoImage(file=image_src)
        self.position = position
        self.rectangle = rectangle

    def move_player(self, direction):
        print(self.position)
        self.position.x += (5 * direction)
        if self.position.x > 570 or self.position.x < 0:
            self.position.x -= (5 * direction)


class Bullet:
    def __init__(self, image_src: str, position: Vector2, rectangle: Rectangle):
        self.image_src = image_src
        self.position = position
        self.rectangle = rectangle


class Meteorite:
    def __init__(self, image_src: str, position: Vector2, rectangle: Rectangle):
        self.image_src = image_src
        self.position = position
        self.rectangle = rectangle
