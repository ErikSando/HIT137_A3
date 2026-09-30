import tkinter as tk
from tkinter import filedialog
from window import Window
from puzzle import Puzzle

# Handles the functionality of the program
class App:
    def __init__(self, window: Window):
        self.window = window
        self.grid_size = 3 #Default Grid 3x3 

    def get_window(self):
        return self.window

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

            if selected_grid == "3 x 3":
                self.grid_size = 3
            elif selected_grid == "4 x 4":
                self.grid_size = 4
            elif selected_grid == "5 x 5":
                self.grid_size = 5

            for widget in self.puzzle_frame.winfo_children():
                widget.destroy()

            #Pass grid size
            self.puzzle = Puzzle(file_path, self.grid_size)
            tk_image = tk.Label(
                self.base_frame,
                image = self.puzzle.get_photoimage()
            )
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