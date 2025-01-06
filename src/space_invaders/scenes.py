from game_classes import *


class MainGameLoop:
    def __init__(self, number_of_enemies: int):
        self.run = True
        self.bullets = []
        self.kill_list = []
        self.meteorites = []
        self.shoot_timer = 0
        self.points = 0
        self.number_of_enemies = number_of_enemies

        self.root, self.canvas = self.create_window()
        self.bg = tk.PhotoImage(file="../../media/space_invaders_background.gif")
        self.canvas.bind_all("a", self.move_player)
        self.canvas.bind_all("<Left>", self.move_player)
        self.canvas.bind_all("d", self.move_player)
        self.canvas.bind_all("<Right>", self.move_player)
        self.canvas.bind_all("<Escape>", self.stop_game)
        self.canvas.bind_all("<space>", self.shoot_bullet)
        self.canvas.bind_all("<Button-1>", self.shoot_bullet)

        self.player = Player(image_src="../../media/player_v2.gif", rectangle=Rectangle(285, 500, 315, 530))
        self.spawn_enemies(self.number_of_enemies)

    def move_player(self, event):
        key = event.keysym
        if key == "a" or key == "Left":
            self.player.move_player(direction=-1)
        elif key == "d" or key == "Right":
            self.player.move_player(direction=1)

    def shoot_bullet(self, event):
        if self.shoot_timer <= 0:
            self.shoot_timer = 50
            print("Shoot")
            bullet = Bullet(image_src="../../media/bullet.gif", rectangle=Rectangle(
                self.player.rectangle.x1 + 12, self.player.rectangle.y1,
                self.player.rectangle.x1 + 18, self.player.rectangle.y1 + 15))
            self.bullets.append(bullet)

    def spawn_enemies(self, num_of_enemies: int):
        for i in range(num_of_enemies):
            if i <= 9:
                k = 0
                yshift = 0
            elif 9 <= i <= 19:
                k = -500
                yshift = 50
            else:
                k = -1000
                yshift = 100
            enemy = Meteorite(image_src="../../media/invader_v1.gif",
                              rectangle=Rectangle(50 + (50 * i) + k, 50 + yshift,
                                                  90 + (50 * i) + k, 90 + yshift))
            self.meteorites.append(enemy)

    def stop_game(self, event):
        self.run = False

    def create_window(self):
        root = tk.Tk()
        canvas = tk.Canvas(root, height=600, width=600, bg="black")
        canvas.pack()

        return root, canvas

    def Update(self):
        global kill_list
        global points

        if len(self.bullets) != 0:
            for bullet in self.bullets:
                bullet.update(self.kill_list, self.meteorites)

        if len(self.kill_list) != 0:
            for kill in self.kill_list:
                self.bullets.remove(kill)
                self.points += 10
            self.kill_list.clear()

        for meteorite in self.meteorites:
            meteorite.update(self.meteorites)

    def Draw(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg)
        self.canvas.create_rectangle(5, 5, 600, 600, outline="black", width="10")
        self.canvas.create_text(60, 20, text=f"Points: {self.points}", font="Arial 14", fill="white")

        if len(self.bullets) != 0:
            for bullet in self.bullets:
                bullet.draw(self.canvas)

        if len(self.meteorites) != 0:
            for meteorite in self.meteorites:
                meteorite.draw(self.canvas)

        self.player.draw(self.canvas)
