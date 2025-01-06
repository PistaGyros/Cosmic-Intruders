import tkinter as tk
from structs import Rectangle


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
        self.is_alive = True

    def kill_itself(self, kill_list: list):
        kill_list.append(self)
        self.is_alive = False

    def on_collision(self, kill_list: list, meteorites: list):
        for meteorite in meteorites:
            if meteorite.rectangle.x1 < self.rectangle.x1 < meteorite.rectangle.x2 \
                    or meteorite.rectangle.x1 < self.rectangle.x2 < meteorite.rectangle.x2:
                if meteorite.rectangle.y1 < self.rectangle.y1 < meteorite.rectangle.y2\
                        or meteorite.rectangle.y1 < self.rectangle.y2 < meteorite.rectangle.y2:
                    print("Collision")
                    meteorites.remove(meteorite)
                    self.kill_itself(kill_list)

        if self.rectangle.y2 <= 0:
            self.kill_itself(kill_list)

    def update(self, kill_list: list, meteorites: list):
        if self.is_alive:
            self.rectangle.y1 -= 5
            self.rectangle.y2 -= 5
            self.on_collision(kill_list, meteorites)

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)


class Meteorite:
    def __init__(self, image_src: str, rectangle: Rectangle):
        self.image = tk.PhotoImage(file=image_src)
        self.rectangle = rectangle
        self.direction = 1
        self.is_alive = True

    def update(self, meteorites: list):
        if self.is_alive:
            self.rectangle.x1 += 0.5 * self.direction
            self.rectangle.x2 += 0.5 * self.direction
            if self.rectangle.x2 >= 595 or self.rectangle.x1 <= 5:
                for meteorite in meteorites:
                    meteorite.direction *= -1
                    meteorite.rectangle.y1 += 10
                    meteorite.rectangle.y2 += 10

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)
