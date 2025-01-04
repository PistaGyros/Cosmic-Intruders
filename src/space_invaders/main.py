from game_classes import *


def move_player(event):
    if event.char == "a":
        player.move_player(direction=-1)
    elif event.char == "d":
        player.move_player(direction=1)


def shoot_bullet(event):
    bullet = Bullet(image_src="../media/bullet.gif", position=player.position)


def close_game(event):
    global run
    run = False


def create_window():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=600, width=600, bg="black")
    canvas.pack()
    return root, canvas


root, canvas = create_window()

player = Player(image_src="../media/player_v2.gif", position=Vector2(285, 500), rectangle=Rectangle(285, 500, 315, 530))
bg = tk.PhotoImage(file="../media/space_invaders_background.gif")
canvas.bind_all("a", move_player)
canvas.bind_all("d", move_player)
canvas.bind_all("<Escape>", close_game)
canvas.bind_all("<space>", shoot_bullet)

run = True
while run:
    # prcni pozadie do funkcie hore nie takto na gadza
    # draw
    canvas.create_image(0, 0, anchor="nw", image=bg)
    canvas.create_image(player.position.x, player.position.y, anchor="nw", image=player.player_img)
    canvas.update()
    canvas.after(10)


root.mainloop()
