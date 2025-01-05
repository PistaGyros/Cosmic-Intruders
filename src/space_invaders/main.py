from game_classes import *


bullets = []
kill_list = []
meteorites = []
shoot_timer = 0


def move_player(event):
    key = event.keysym
    if key == "a" or key == "Left":
        player.move_player(direction=-1)
    elif key == "d" or key == "Right":
        player.move_player(direction=1)


def shoot_bullet(event):
    global shoot_timer
    if shoot_timer <= 0:
        shoot_timer = 50
        print("Shoot")
        bullet = Bullet(image_src="../../media/bullet.gif", rectangle=Rectangle(
            player.rectangle.x1 + 12, player.rectangle.y1,
            player.rectangle.x1 + 18, player.rectangle.y1 + 15))
        bullets.append(bullet)


def spawn_enemies(num_of_enemies: int):
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
        meteorites.append(enemy)


def stop_game(event):
    global run
    run = False


def create_window():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=600, width=600, bg="black")
    canvas.pack()

    return root, canvas


root, canvas = create_window()
bg = tk.PhotoImage(file="../../media/space_invaders_background.gif")

player = Player(image_src="../../media/player_v2.gif", rectangle=Rectangle(285, 500, 315, 530))
spawn_enemies(30)

# Binds
canvas.bind_all("a", move_player)
canvas.bind_all("<Left>", move_player)
canvas.bind_all("d", move_player)
canvas.bind_all("<Right>", move_player)
canvas.bind_all("<Escape>", stop_game)
canvas.bind_all("<space>", shoot_bullet)
canvas.bind_all("<Button-1>", shoot_bullet)


def Update():
    global kill_list

    if len(bullets) != 0:
        for bullet in bullets:
            bullet.update(kill_list, meteorites)

    if len(kill_list) != 0:
        for kill in kill_list:
            bullets.remove(kill)
        kill_list.clear()

    for meteorite in meteorites:
        meteorite.update(meteorites)


def Draw():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=bg)
    canvas.create_rectangle(5, 5, 600, 600, outline="black", width="10")
    canvas.create_text(60, 20, text=f"Points: {(30 - len(meteorites)) * 10}", font="Arial 14", fill="white")

    if len(bullets) != 0:
        for bullet in bullets:
            bullet.draw(canvas)

    if len(meteorites) != 0:
        for meteorite in meteorites:
            meteorite.draw(canvas)

    player.draw(canvas)


run = True
while run:
    Update()
    Draw()
    shoot_timer -= 1
    canvas.update()
    canvas.after(10)


root.mainloop()
