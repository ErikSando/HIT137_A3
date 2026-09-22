from window import *
from puzzle import *

def main():
    window = Window("Game", 800, 600)

    thing = Puzzle("res/image1.jpg")

    label = tk.Label(window, image=thing.get_image())
    label.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
