import tkinter as tk
from window import *
from puzzle import *

# Handles the functionality of the program
class App:
    def __init__(self, window: Window):
        self.window = window

    def start(self):
        puzzle = Puzzle("res/image1.jpg")

        for row in puzzle.tiles:
            for tile in row:
                label = tk.Label(self.window, image = tile.get_image())
                label.pack()

        self.window.mainloop()