import tkinter as tk
from window import *
from puzzle import *

# Handles the functionality of the program
class App:
    def __init__(self, window: Window):
        self.window = window

    def start(self):
        # Testing functionality
        puzzle = Puzzle("res/image1.jpg")

        frame = tk.Frame(self.window)

        i = 0

        for row in puzzle.tiles:
            j = 0
            for tile in row:
                tile.rotate(i)
                label = tk.Label(frame, image = tile.get_photoimage())
                label.grid(row=i, column=j)
                j += 1
            i += 1

        frame.pack()

        self.window.mainloop()