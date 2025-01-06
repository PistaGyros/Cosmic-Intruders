from game_classes import *
import time


class MainGameScene:
    def __init__(self, root, canvas, main_menu_scene, difficulty: int, number_of_enemies: int):
        self.root = root
        self.canvas = canvas
        self.main_menu_scene = main_menu_scene
        self.actual_difficulty = difficulty
        self.number_of_enemies = number_of_enemies
        self.run = True
        self.bullets = []
        self.kill_list = []
        self.meteorites = []
        self.shoot_timer = 0
        self.points = 0
        self.stopwatch = time.time()
        self.actual_time = 0

        self.bg = tk.PhotoImage(file="../../media/space_invaders_background.gif")
        self.input_field = tk.Entry(self.root)

        # Binds
        self.canvas.bind_all("a", self.move_player)
        self.canvas.bind_all("<Left>", self.move_player)
        self.canvas.bind_all("d", self.move_player)
        self.canvas.bind_all("<Right>", self.move_player)
        self.canvas.bind_all("<Escape>", self.stop_game)
        self.canvas.bind_all("<space>", self.shoot_bullet)
        self.canvas.bind_all("<Button-1>", self.shoot_bullet)
        self.canvas.bind_all("m", self.kill_every_enemy)

        self.player = Player(image_src="../../media/player_v2.gif", rectangle=Rectangle(285, 500, 315, 530))
        self.spawn_enemies(self.number_of_enemies)

    def kill_every_enemy(self, event):
        self.meteorites.clear()

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

    def create_ui(self):
        self.canvas.create_text(60, 20, text=f"Points: {self.points}", font="Arial 14", fill="white")
        self.actual_time = int(time.time() - self.stopwatch)
        self.canvas.create_text(540, 20, text=f"Time: {self.actual_time}", font="Arial 14", fill="white")

    def on_enter(self, event):
        input_name = self.input_field.get()
        file = open("../../media/leaderboard.txt", "a")
        file.write(f"\n{input_name}, {self.actual_difficulty}, {self.points}, {self.actual_time}")
        file.close()
        leaderboard_scene = LeaderBoard(self.root, self.canvas, "../../media/leaderboard.txt")
        leaderboard_scene.Draw(self.main_menu_scene)

    def end_game_frame(self):
        print("YOU WON")
        self.canvas.delete("all")
        self.canvas.create_text(300, 300, text="YOU WON", font="Arial 14", fill="white")
        self.input_field.insert(0, "Write your nickname")
        self.canvas.create_window(300, 320, window=self.input_field)
        self.canvas.bind_all("<Return>", self.on_enter)


    def Update(self):
        self.shoot_timer -= 1

        if len(self.bullets) != 0:
            for bullet in self.bullets:
                bullet.update(self.kill_list, self.meteorites)

        if len(self.kill_list) != 0:
            for kill in self.kill_list:
                self.bullets.remove(kill)
                self.points += 10
            self.kill_list.clear()

        if len(self.meteorites) > 0:
            for meteorite in self.meteorites:
                meteorite.update(self.meteorites)
        elif len(self.meteorites) <= 0:
            # You won, the end
            self.run = False
            self.end_game_frame()

    def Draw(self):
        self.canvas.delete("all")

        self.canvas.create_image(0, 0, anchor="nw", image=self.bg)
        self.canvas.create_rectangle(5, 5, 600, 600, outline="black", width="10")
        self.create_ui()

        if len(self.bullets) != 0:
            for bullet in self.bullets:
                bullet.draw(self.canvas)

        if len(self.meteorites) != 0:
            for meteorite in self.meteorites:
                meteorite.draw(self.canvas)

        self.player.draw(self.canvas)


class MainMenuScene:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.Draw()

    def Draw(self):
        self.canvas.delete("all")
        start_button = tk.Button(self.root, text="Start Game", bg="white", command=self.main_game_loop_button)
        self.canvas.create_window(290, 290, window=start_button)
        leaderboard_button = tk.Button(self.root, text="LeaderBoard", bg="white", command=self.leaderbutton)
        self.canvas.create_window(290, 320, window=leaderboard_button)

    def main_game_loop_button(self):
        game_scene = MainGameScene(self.root, self.canvas, self, difficulty=1, number_of_enemies=30)
        self.main_game_loop(game_scene)

    def main_game_loop(self, scene):
        while scene.run:
            scene.Draw()
            scene.Update()
            scene.canvas.update()
            scene.canvas.after(25)

    def leaderbutton(self):
        leaderboard_scene = LeaderBoard(self.root, self.canvas, "../../media/leaderboard.txt")
        leaderboard_scene.Draw(self)


class LeaderBoard:
    def __init__(self, root, canvas, leaderboard_file_path):
        self.root = root
        self.canvas = canvas
        self.file_path = leaderboard_file_path
        self.names = []
        self.difficulties = []
        self.points = []
        self.times = []

    def read_file(self, file_path):
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()
        for line in lines:
            words = line.strip().split(", ")
            self.names.append(words[0])
            self.difficulties.append(words[1])
            self.points.append(words[2])
            self.times.append(words[3])

    def Draw(self, main_scene):
        self.canvas.delete("all")
        self.canvas.create_text(300, 50, text="LeaderBoard", font="Arial 18", fill="white")
        self.read_file(self.file_path)
        for i in range(len(self.names)):
            self.canvas.create_text(300, 50 * i + 100, text=f"{i + 1}. Meno: {self.names[i]} uroven: {self.difficulties[i]} "
                                                      f"points: {self.points[i]} čas: {self.times[i]}", fill="white",
                                    font="Arial 14")
        leave_button = tk.Button(self.root, text="Main Menu", command=main_scene.Draw)
        self.canvas.create_window(50, 50, window=leave_button)
