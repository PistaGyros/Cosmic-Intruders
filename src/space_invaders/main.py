from scenes import *


# Create main window
def create_window():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=600, width=600, bg="black")
    canvas.pack()

    return root, canvas


root, canvas = create_window()
main_scene = MainMenuScene(root, canvas)
root.mainloop()
