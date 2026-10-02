import tkinter as tk
import random
from tkinter import filedialog
from tkinter import ttk
import config
from menu import MenuElem, Menu
from game_controller import GameController
from game_controller_ui import GameControllerUI
from puzzle import Puzzle
from transformations import TransformationInfo, Swap, Rotate, HorizontalFlip, VerticalFlip

# Handles the functionality of the program
class App:
    def __init__(self, title: str, width: int, height: int):
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(f"{width}x{height}")
        self.window.configure(bg="#F4F4F0")

        self.grid_choice = tk.StringVar()
        self.grid_choice.set(config.DEFAULT_GRID_SIZE)
        self.grid_size = 3 # Default Grid 3x3

        self.labels = []
        self.gamecontroller_ui = None
        self.last_locked = False
        self.show_completion =True

        back_button = MenuElem(tk.Button(self.window, text = "<", font = ("Arial", 12, "bold"), command = lambda *_: self.show_menu("start")), "place", x = 5, y = 5, width = 25, height = 25)

        start_title = tk.Label(
            self.window,
            text="Welcome to the Image Puzzle Game!",
            font=("Arial", 17, "bold"),
            bg="#F4F4F0"
        )

        grid_option_text = tk.Label(
            self.window,
            text = "Choose Puzzle Size:",
            bg="#F4F4F0",
        )

        grid_option_menu = tk.OptionMenu(
            self.window,
            self.grid_choice,
            "3 x 3",
            "4 x 4",
            "5 x 5",
        )
        grid_option_menu.configure(
            background="#F4F4F0",
            foreground="black",
            activebackground="#F4F4F0",
            activeforeground="black"
        )
        grid_option_menu["menu"].configure(
            background="#F4F4F0",
            foreground="black",
            activebackground="#F4F4F0",
            activeforeground="black"
        )

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custome.TButton",
            background="#3A5A40", #7593AD
            foreground="#FFFFFF",
            anchor = "center"
        )

        style.map(
            "Custome.TButton",
            background=[
                ("active", "#3A5A40"),
                ("pressed", "#3A5A40")
            ],
            foreground=[
                ("active", "white"),
                ("pressed", "white")
            ]
        )
        open_button = ttk.Button(self.window, text="Click to Select Image", command=self.open_puzzle, style="Custome.TButton")
        
        self.puzzle_frame = tk.Frame(self.window, bg="#F4F4F0")
        self.grid_frame = tk.Frame(self.puzzle_frame, bg="#F4F4F0")
        self.grid_frame.grid(row=0, column=1, padx=25, pady=50)

        puzzle_title = tk.Label(
            self.window,
            text="Image Puzzle Game",
            font=("Arial", 17, "bold"),
            bg="#F4F4F0"
        )

        start_menu_elements = [
            MenuElem(start_title, "pack", pady=(100, 10)),
            MenuElem(grid_option_text, "pack", pady=(10, 5)),
            MenuElem(grid_option_menu, "pack", pady=5),
            MenuElem(open_button, "pack", pady=20)
        ]

        puzzle_menu_elements = [
            back_button,
            MenuElem(puzzle_title, "pack", pady=(15, 5)),
            MenuElem(self.puzzle_frame, "pack")
        ]

        self.menus = {
            "start": Menu(self.window, start_menu_elements, visible = True),
            "puzzle": Menu(self.window, puzzle_menu_elements)
        }

    def get_window(self):
        return self.window

    def update(self):
        get_locked = getattr(self, "last_locked", self.gc.locked)
        if self.gamecontroller_ui is not None:
            self.gamecontroller_ui.display_images = []

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                position = (r, c)
                bg_colour = config.OUTLINE_COLOURS["default"]

                if position == self.gc.selected_position:
                    bg_colour = config.OUTLINE_COLOURS["selected"]

                if self.gamecontroller_ui is not None:
                    image = self.gamecontroller_ui.tile_displayed(position)

                else:
                    image = self.puzzle.get_tile(position).get_photoimage()
                self.labels[r][c].configure(image=image, bg=bg_colour)

        if self.gamecontroller_ui is not None:
            self.gamecontroller_ui.update_info()
            self.gamecontroller_ui.update_original_image(self.tk_image)

            if self.show_completion:
                self.gamecontroller_ui.check_completion(get_locked)

        self.last_locked = self.gc.locked

    def show_menu(self, name: str):
        for menu_name in self.menus:
            self.menus[menu_name].hide()

        self.menus[name].show()

    def open_puzzle(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
        )

        if file_path:
            self.show_menu("puzzle")

            # Get the grid size selected by the user
            selected_grid = self.grid_choice.get()

            self.grid_size = config.GRID_CONFIG[selected_grid]["size"]

            for widget in self.grid_frame.winfo_children():
                widget.destroy()

            #Pass grid size
            self.puzzle = Puzzle(file_path, self.grid_size)
            self.tk_image = tk.Label(
                self.puzzle_frame,
                image = self.puzzle.get_photoimage()
            )
            self.tk_image.grid(row=0, column=0, padx=25, pady=50)

            self.gc = GameController(self.puzzle)

            transformations = [ Swap(), Rotate(), VerticalFlip(), HorizontalFlip() ]

            # Pick the number of transformations based on the grid size
            n_transformations = config.GRID_CONFIG[selected_grid]["transformations"]

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
                    label = tk.Label(self.grid_frame, image=tile.get_photoimage(), borderwidth=1, bg=config.OUTLINE_COLOURS["default"])
                    label.grid(row=r, column=c)
                    label.bind("<Button-1>", lambda e, r=r, c=c: [self.gc.handle_left_click((r, c)), self.update()])
                    label.bind("<Shift-Button-1>", lambda e, r=r, c=c: [self.gc.handle_shift_click((r, c)), self.update()])
                    label.bind("<Button-3>", lambda e, r=r, c=c: [self.gc.handle_right_click((r, c)), self.update()])
                    self.labels[r][c] = label
                    c += 1

                r += 1
            self.gamecontroller_ui = GameControllerUI(
                self.puzzle,
                self.gc,
                self.puzzle_frame
            )

            self.gamecontroller_ui.set_app(self)
            self.gamecontroller_ui.build()
            self.update()

    def start(self):
        self.window.mainloop()