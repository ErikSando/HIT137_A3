import tkinter as tk
import random
from tkinter import filedialog

import config
from game_controller import GameController
from window import Window
from puzzle import Puzzle
from transformations import TransformationInfo, Swap, Rotate, HorizontalFlip, VerticalFlip

# Handles the functionality of the program
class App:
    def __init__(self, window: Window):
        self.window = window
        self.grid_size = 3 # Default Grid 3x3
        self.labels = []

    def get_window(self):
        return self.window

    def update(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                bg_colour = config.OUTLINE_COLOURS["default"]

                position = (r, c)

                if position == self.gc.selected_position:
                    bg_colour = config.OUTLINE_COLOURS["selected"]

                self.labels[r][c].configure(image=self.puzzle.get_tile(position).get_photoimage(), bg=bg_colour)

    def label_left_click(self, position: tuple[int, int]):
        self.gc.handle_left_click(position)
        self.update()

    def label_right_click(self, position: tuple[int, int]):
        self.gc.handle_right_click(position)
        self.update()

    def label_shift_click(self, position: tuple[int, int]):
        self.gc.handle_shift_click(position)
        self.update()

    def open_puzzle(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )

        if file_path:
            self.firstheader.pack_forget()
            self.grid_option.pack_forget()
            self.grid_menu.pack_forget()
            self.open_button.pack_forget()

            self.welcomepage.pack(
                side = tk.TOP,
                pady=20
            )

            self.base_frame.pack(side=tk.TOP)

            # Get the grid size selected by the user
            selected_grid = self.grid_choice.get()

            self.grid_size = config.GRID_SIZE[selected_grid]

            for widget in self.puzzle_frame.winfo_children():
                widget.destroy()

            #Pass grid size
            self.puzzle = Puzzle(file_path, self.grid_size)
            tk_image = tk.Label(
                self.base_frame,
                image = self.puzzle.get_photoimage()
            )
            tk_image.grid(row=0, column=0, padx=25, pady=50)

            self.gc = GameController(self.puzzle)

            transformations = [ Swap(), Rotate(), VerticalFlip(), HorizontalFlip() ]

            # Pick the number of transformations based on the grid size
            n_transformations = config.N_TRANSFORMATIONS[self.grid_size]

            for _ in range(n_transformations):
                t_info = TransformationInfo(
                    self.puzzle,
                    [
                        (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)),
                        (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
                    ],
                    random.randint(1, 3)
                )

                t = random.choice(transformations)
                t.apply(t_info)

            self.labels = [ [ None for _ in range(self.grid_size) ] for _ in range(self.grid_size) ]

            r = 0

            for row in self.puzzle.tiles:
                c = 0

                self.labels.append([])

                for tile in row:
                    label = tk.Label(self.puzzle_frame, image=tile.get_photoimage(), borderwidth=1, bg=config.OUTLINE_COLOURS["default"])
                    label.grid(row=r, column=c)
                    label.bind("<Button-1>", lambda e, r=r, c=c: self.label_left_click((r, c)))
                    label.bind("<Shift-Button-1>", lambda e, r=r, c=c: self.label_shift_click((r, c)))
                    label.bind("<Button-3>", lambda e, r=r, c=c: self.label_right_click((r, c)))
                    self.labels[r][c] = label
                    c += 1

                r += 1

    def grid_size_change(self, size):
        self.grid_size = size

    def start(self):
        #Welcome Label
        self.top_frame = tk.Frame(self.window)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.welcomepage = tk.Label(
            self.top_frame,
            text="Welcome to the Image Puzzle Game!",
            font=("Arial", 17, "bold")
        )

        self.base_frame = tk.Frame(self.window)
        self.puzzle_frame = tk.Frame(self.base_frame)
        self.puzzle_frame.grid(row=0, column=1, padx=25, pady=50)
        self.base_frame.pack()

        # Image selection instruction
        self.firstheader = tk.Label(
            self.window,
            text="Image Puzzle Game",
            font=("Arial", 17, "bold")
        )
        self.firstheader.pack(pady=(15, 5))

        ###Grid size selection
        self.grid_option = tk.Label(
            self.window,
            text = "Choose Puzzle Size:"
        )
        self.grid_option.pack(pady=(10, 5))
        # Variable that stores the user's selection
        self.grid_choice = tk.StringVar()
        self.grid_choice.set("3 x 3")   # Default selection
        # Dropdown menu
        self.grid_menu = tk.OptionMenu(
            self.window,
            self.grid_choice,
            "3 x 3",
            "4 x 4",
            "5 x 5"
        )
        self.grid_menu.pack(pady=5)
        
        self.open_button = tk.Button(self.window, text="Click to Select Image", command=self.open_puzzle)
        self.open_button.pack(pady=20)

        self.window.mainloop()