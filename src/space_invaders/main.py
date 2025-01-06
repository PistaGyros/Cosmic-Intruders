from scenes import *


game_loop_scene = MainGameLoop(30)


def main_game_loop(scene):
    while scene.run:
        scene.Update()
        scene.Draw()
        scene.shoot_timer -= 1
        scene.canvas.update()
        scene.canvas.after(25)

    scene.root.mainloop()


main_game_loop(game_loop_scene)
