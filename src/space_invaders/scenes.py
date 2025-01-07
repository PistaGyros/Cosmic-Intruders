from game_classes import *
import time
import tkinter.scrolledtext


class MainGameScene:
    def __init__(self, root, canvas, main_menu_scene, difficulty: int):
        self.root = root
        self.canvas = canvas
        self.main_menu_scene = main_menu_scene
        self.actual_difficulty = difficulty
        self.run = True
        self.bullets = []
        self.kill_list = []
        self.meteorites = []
        self.shoot_timer = 0
        self.points = 0
        self.stopwatch = time.time()
        self.actual_time = 0
        self.previus_frame_time = self.stopwatch
        self.delta_time = 0

        self.bg = tk.PhotoImage(file="../../media/space_invaders_background.gif")
        self.input_field = tk.Entry(self.root)

        # Binds
        self.canvas.bind_all("a", lambda event, direction = -1: self.move_player(event, direction))
        self.canvas.bind_all("<Left>", lambda event, direction = -1: self.move_player(event, direction))
        self.canvas.bind_all("d", lambda event, direction = 1: self.move_player(event, direction))
        self.canvas.bind_all("<Right>", lambda event, direction = 1: self.move_player(event, direction))
        self.canvas.bind_all("<space>", self.shoot_bullet)
        self.canvas.bind_all("<Button-1>", self.shoot_bullet)
        self.canvas.bind_all("m", self.kill_every_enemy)

        self.player = Player(image_src="../../media/player_v2.gif", rectangle=Rectangle(285, 500, 315, 530))
        self.spawn_enemies(self.actual_difficulty)

    # Cheat code
    def kill_every_enemy(self, event):
        self.points = len(self.meteorites) * 10
        self.meteorites.clear()

    def move_player(self, event, direction):
        self.player.move_player(self.delta_time, direction)

    def shoot_bullet(self, event):
        if self.shoot_timer >= 50 or len(self.bullets) == 0:
            self.shoot_timer = 0
            bullet = Bullet(image_src="../../media/bullet.gif", rectangle=Rectangle(
                self.player.rectangle.x1 + 12, self.player.rectangle.y1,
                self.player.rectangle.x1 + 18, self.player.rectangle.y1 + 15))
            self.bullets.append(bullet)

    def spawn_enemies(self, difficulty: int):
        xshift = 0
        yshift = 0
        yshift_add, num_of_enemies, speed_add = self.change_parameters_on_difficulty(difficulty)
        for i in range(num_of_enemies):
            if i % 10 == 0 and i != 0:
                xshift -= 500
                yshift += 50
            enemy = Meteorite(image_src="../../media/invader_v1.gif",
                              rectangle=Rectangle(50 + (50 * i) + xshift, 50 + yshift,
                                                  90 + (50 * i) + xshift, 90 + yshift), speed_add=speed_add)
            self.meteorites.append(enemy)

    def change_parameters_on_difficulty(self, difficulty: int):
        yshift_add, num_of_enemies, speed_add = 0, 0, 0
        if difficulty == 1:
            yshift_add = 50
            num_of_enemies = 10
            speed_add = 0.75
        elif difficulty == 2:
            yshift_add = 50
            num_of_enemies = 20
            speed_add = 1
        elif difficulty == 3:
            yshift_add = 50
            num_of_enemies = 30
            speed_add = 1.25
        elif difficulty == 4:
            yshift_add = 100
            num_of_enemies = 20
            speed_add = 1
        elif difficulty == 5:
            yshift_add = -500
            num_of_enemies = 50
            speed_add = 1.5
        return yshift_add, num_of_enemies, speed_add

    def stop_game(self, event):
        self.run = False

    def create_ui(self):
        self.canvas.create_text(60, 20, text=f"Points: {self.points}", font="Arial 14", fill="white")
        self.actual_time = int(time.time() - self.stopwatch)
        self.canvas.create_text(540, 20, text=f"Time: {self.actual_time}", font="Arial 14", fill="white")
        self.canvas.create_rectangle(500, 540, 500 + (80 * (self.shoot_timer / 50)), 560, fill="yellow")

    def on_enter(self, event):
        input_name = self.input_field.get()
        file = open("../../media/leaderboard.txt", "a")
        file.write(f"\n{input_name}, {self.actual_difficulty}, {self.points}, {self.actual_time}")
        file.close()
        leaderboard_scene = LeaderBoard(self.root, self.canvas, self, "../../media/leaderboard.txt")
        leaderboard_scene.Draw(self.main_menu_scene)

    def end_game_frame(self, win_or_lose):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg)
        self.canvas.create_text(300, 300, text="YOU WON" if win_or_lose else "GAME OVER", font="Arial 14", fill="white")
        self.input_field.insert(0, "Write your nickname")
        self.canvas.create_window(300, 320, window=self.input_field)
        self.canvas.bind_all("<Return>", self.on_enter)

    def change_direction_of_meteorites(self):
        for meteorite in self.meteorites:
            meteorite.direction *= -1
            meteorite.rectangle.x1 += 33 * meteorite.direction * meteorite.speed_add * self.delta_time
            meteorite.rectangle.x2 += 33 * meteorite.direction * meteorite.speed_add * self.delta_time
            meteorite.rectangle.y1 += 5
            meteorite.rectangle.y2 += 5


    def calculate_delta_time(self):
        delta_time = time.time() - self.previus_frame_time
        self.previus_frame_time = time.time()
        return delta_time

    def Update(self):
        self.delta_time = self.calculate_delta_time()
        if self.shoot_timer >= 51:
            self.shoot_timer = 51
        else:
            self.shoot_timer += 1

        if len(self.bullets) != 0:
            for bullet in self.bullets:
                bullet.update(self, self.delta_time, self.kill_list, self.meteorites)

        if len(self.kill_list) != 0:
            for kill in self.kill_list:
                self.bullets.remove(kill)
            self.kill_list.clear()

        if len(self.meteorites) > 0:
            meteorites_change_direct = False
            for meteorite in self.meteorites:
                meteorite.update(self.delta_time, self.player.rectangle, self.meteorites, self)
                if meteorite.rectangle.x2 > 590 or meteorite.rectangle.x1 < 10:
                    meteorites_change_direct = True
            if meteorites_change_direct:
                self.change_direction_of_meteorites()
        elif len(self.meteorites) <= 0:
            # You won, the end
            self.run = False
            self.end_game_frame(True)

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
        self.bg = tk.PhotoImage(file="../../media/space_invaders_background.gif")
        self.actual_diff = 1
        self.diff_buttons = []
        self.Draw()

    def Draw(self):
        self.canvas.delete("all")
        self.diff_buttons.clear()
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg)
        self.canvas.create_text(300, 150, text="Cosmic\nIntruders", font="Times 50", fill="yellow", justify="center")
        start_button = tk.Button(self.root, text="Start Game", bg="white", command=self.main_game_loop_button)
        self.canvas.create_window(300, 290, window=start_button)
        # level buttons
        self.create_difficulties_buttons()
        leaderboard_button = tk.Button(self.root, text="LeaderBoard", bg="white", command=self.leaderbutton)
        self.canvas.create_window(300, 350, window=leaderboard_button)
        self.canvas.create_text(
            300, 500, text="A/D Left/Right | <space> Shoot", font="Arial 30", fill="black", justify="center")

    def create_difficulties_buttons(self):
        self.diff_buttons.append(tk.Button(self.root, text="1", bg="green", command=lambda: self.change_difficulty(0)))
        self.diff_buttons.append(tk.Button(self.root, text="2", command=lambda: self.change_difficulty(1)))
        self.diff_buttons.append(tk.Button(self.root, text="3", command=lambda: self.change_difficulty(2)))
        self.diff_buttons.append(tk.Button(self.root, text="4", command=lambda: self.change_difficulty(3)))
        self.diff_buttons.append(tk.Button(self.root, text="5", command=lambda: self.change_difficulty(4)))
        for i in range(len(self.diff_buttons)):
            self.canvas.create_window(260 + i * 20, 320, window=self.diff_buttons[i])

    def change_difficulty(self, pressed_button_index):
        self.actual_diff = pressed_button_index + 1
        for button in self.diff_buttons:
            button.config(bg="white")
        self.diff_buttons[pressed_button_index].config(bg="green")

    def main_game_loop_button(self):
        game_scene = MainGameScene(self.root, self.canvas, self, difficulty=self.actual_diff)
        self.main_game_loop(game_scene)

    def main_game_loop(self, scene):
        while scene.run:
            scene.Draw()
            scene.Update()
            scene.canvas.update()
            scene.canvas.after(1)

    def leaderbutton(self):
        leaderboard_scene = LeaderBoard(self.root, self.canvas, self, "../../media/leaderboard.txt")
        leaderboard_scene.Draw(self)


class LeaderBoard:
    def __init__(self, root, canvas, main_scene, leaderboard_file_path):
        self.root = root
        self.canvas = canvas
        self.file_path = leaderboard_file_path
        self.names = []
        self.difficulties = []
        self.points = []
        self.times = []
        self.bg = tk.PhotoImage(file="../../media/space_invaders_background.gif")
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg)

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
        self.canvas.create_text(340, 50, text="LeaderBoard", font="Arial 18", fill="white")
        self.read_file(self.file_path)
        scrollable_leaderboard = tk.scrolledtext.ScrolledText(self.root, width=40, bg="cornflower blue", font="Arial 14")
        for i in range(len(self.names)):
            scrollable_leaderboard.insert(tk.INSERT, f"{i + 1}. Meno: {self.names[i]}, úroveň: "
                                                     f"{self.difficulties[i]}, body: {self.points[i]}, "
                                                     f"čas: {self.times[i]}\n", "text")
        scrollable_leaderboard.tag_configure("text", justify="center")
        scrollable_leaderboard.configure(state="disabled")
        self.canvas.create_window(340, 330, window=scrollable_leaderboard)
        leave_button = tk.Button(self.root, text="Main Menu", command=main_scene.Draw)
        self.canvas.create_window(50, 50, window=leave_button)
