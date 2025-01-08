import tkinter as tk
from structs import Rectangle


class Player:
    def __init__(self, image_src: str, rectangle: Rectangle):
        self.image = tk.PhotoImage(file=image_src)
        self.rectangle = rectangle

    def move_player(self, delta_time: float, direction):
        self.rectangle.x1 += (200 * direction) * delta_time
        self.rectangle.x2 += (200 * direction) * delta_time
        if self.rectangle.x1 > 570 or self.rectangle.x1 < 0:
            self.rectangle.x1 -= (200 * direction) * delta_time
            self.rectangle.x2 -= (200 * direction) * delta_time

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

    def on_collision(self, game_scene, kill_list: list, meteorites: list):
        for meteorite in meteorites:
            if OnCollision.on_collision(meteorite.rectangle, self.rectangle):
                meteorites.remove(meteorite)
                game_scene.points += 10
                self.kill_itself(kill_list)

        if self.rectangle.y2 <= 0:
            self.kill_itself(kill_list)
            game_scene.points -= 5

    def update(self, game_scene,  delta_time: float, kill_list: list, meteorites: list):
        if self.is_alive:
            self.rectangle.y1 -= 200 * delta_time
            self.rectangle.y2 -= 200 * delta_time
            self.on_collision(game_scene, kill_list, meteorites)

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)


class Meteorite:
    def __init__(self, image_src: str, rectangle: Rectangle, speed_add: float):
        self.image = tk.PhotoImage(file=image_src)
        self.rectangle = rectangle
        self.speed_add = speed_add
        self.direction = 1
        self.is_alive = True

    def update(self,  delta_time: float, player_rectangle, game_scene):
        if self.is_alive:
            self.rectangle.x1 += 33 * self.direction * self.speed_add * delta_time
            self.rectangle.x2 += 33 * self.direction * self.speed_add * delta_time

            if OnCollision.on_collision(player_rectangle, self.rectangle):
                # Gave over
                game_scene.run = False
                game_scene.end_game_frame(False)

    def draw(self, canvas):
        canvas.create_image(self.rectangle.x1, self.rectangle.y1, anchor="nw", image=self.image)


class OnCollision:

    @staticmethod
    def on_collision(first_rectangle, second_rectangle):
        if first_rectangle.x1 < second_rectangle.x1 < first_rectangle.x2 \
                or first_rectangle.x1 < second_rectangle.x2 < first_rectangle.x2:
            if first_rectangle.y1 < second_rectangle.y1 < first_rectangle.y2 \
                    or first_rectangle.y1 < second_rectangle.y2 < first_rectangle.y2:
                return True
        else:
            return False
