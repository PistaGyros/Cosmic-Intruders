from game_classes import *


bullets = []
kill_list = []
meteorites = []


def move_player(event):
    if event.char == "a":
        player.move_player(direction=-1)
    elif event.char == "d":
        player.move_player(direction=1)


def shoot_bullet(event):
    print("Shoot")
    bullet = Bullet(image_src="../../media/bullet.gif", rectangle=Rectangle(
                              player.rectangle.x1 + 10, player.rectangle.y1,
                              player.rectangle.x2 + 10, player.rectangle.y2))
    bullets.append(bullet)


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

# Binds
canvas.bind_all("a", move_player)
canvas.bind_all("d", move_player)
canvas.bind_all("<Escape>", stop_game)
canvas.bind_all("<space>", shoot_bullet)


def Update():
    global kill_list
    if len(bullets) != 0:
        for bullet in bullets:
            bullet.update(kill_list)
    if len(kill_list) != 0:
        for kill in kill_list:
            bullets.remove(kill)
        kill_list = bullets.copy()


def Draw():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=bg)

    if len(bullets) != 0:
        for bullet in bullets:
            bullet.draw(canvas)

    player.draw(canvas)


run = True
while run:
    Update()
    Draw()
    canvas.update()
    canvas.after(10)


root.mainloop()
