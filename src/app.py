import tkinter as tk
from tkinter import filedialog
from window import *
from puzzle import *

# Handles the functionality of the program
class App:
    def __init__(self, window: Window):
        self.window = window

    def get_window(self):
        return self.window

    def open_puzzle(self):
        file_path = filedialog.askopenfilename(
                title="Select an Image",
                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
            )

        if file_path:
            self.puzzle = Puzzle(file_path)

            tk_image = tk.Label(self.base_frame, image=self.puzzle.get_photoimage())
            tk_image.grid(row=0, column=0, padx=25, pady=50)

            i = 0

            for row in self.puzzle.tiles:
                j = 0

                for tile in row:
                    # apply a transformation here, alternatively apply the transformation automatically in the Tile class
                    label = tk.Label(self.puzzle_frame, image = tile.get_photoimage(), borderwidth=1, bg="lightblue")
                    label.grid(row=i, column=j)
                    j += 1

                i += 1

    def start(self):
        self.base_frame = tk.Frame(self.window)
        self.puzzle_frame = tk.Frame(self.base_frame)
        self.puzzle_frame.grid(row=0, column=1, padx=25, pady=50)
        self.base_frame.pack()

        self.open_button = tk.Button(self.window, text="Choose Image", command=self.open_puzzle)
        self.open_button.pack(pady=20)

        self.window.mainloop()