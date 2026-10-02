import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageDraw, ImageTk
from tkinter import ttk

# Additional Game UI for player convenience
class GameControllerUI:

    def __init__(
        self,
        puzzle,
        controller,
        main_frame
    ):
        self.puzzle = puzzle
        self.controller = controller
        self.main_frame = main_frame
        self.gameui_frame = None
        self.move_label = None
        self.incorrect_tiles = None
        self.hint_label = None
        self.hint_btn = None
        self.solve_btn = None
        self.display_images = []

        self.original_display_image = None    # Original image displaying hint

    def build(self):
        self.ui_controls()

    def ui_controls(self):
        self.gameui_frame = tk.Frame(self.main_frame, bg="#F4F4F0")
        self.gameui_frame.grid(row=1, column=0, columnspan=2, pady=(10, 15))
        self.move_label = tk.Label(self.gameui_frame, text="Moves: 0", font=("Arial", 12), bg="#F4F4F0")
        self.move_label.grid(row=0, column=0, padx=15)

        #Count for incorrect tiles
        self.incorrect_tiles = tk.Label(self.gameui_frame, text="Incorrect tiles: 0", font=("Arial", 12), bg="#F4F4F0")
        self.incorrect_tiles.grid(row=0, column=1, padx=15)

        #Number of Hints available and Button
        self.hint_label = tk.Label(self.gameui_frame, text="Hints Available: 3", font=("Arial", 12), bg="#F4F4F0")
        self.hint_label.grid(row=0, column=2,padx=15)
            
        self.hint_btn = ttk.Button(self.gameui_frame, text="Hint", command=self.hint_option, style="Custome.TButton")
        self.hint_btn.grid(row=1,column=1, pady=40, padx=(0, 100))

        #solve Button
        self.solve_btn = ttk.Button(self.gameui_frame, text="Solve", command=self.solve_option, style="Custome.TButton")
        self.solve_btn.grid(row=1, column=2, pady=40, padx=(5, 20))

    def hint_option(self):
        self.controller.use_hint()
        self.refresh_app()

    def solve_option(self):       
        self.controller.solve()
        self.app.show_completion = False
        self.refresh_app()
        self.app.show_completion = True

    def refresh_app(self):
        if hasattr(self, "app") and self.app is not None:
            self.app.update()
        else:
            self.update_info()

    def set_app(self, app):
        self.app = app

    def update_info(self):
        if self.move_label is not None:
            self.move_label.configure(
                text=f"Moves: {self.controller.moves}"
            )
        if self.incorrect_tiles is not None:
            self.incorrect_tiles.configure(
                text=(
                    f"Incorrect tiles: "
                    f"{self.controller.tiles_incorrect()}"
                )
            )
        if self.hint_label is not None:
            self.hint_label.configure(
                text=(
                    f"Hints remaining: "
                    f"{self.controller.hints_remaining()}"
                )
            )
        self.update_btn_state()

    def update_btn_state(self):
        if self.controller.locked:
            self.hint_btn.configure(state="disabled")
            self.solve_btn.configure(state="disabled")
        else:
            if self.controller.hints_remaining() > 0:
                self.hint_btn.configure(state="normal")
            else:
                self.hint_btn.configure(state="disabled")
            self.solve_btn.configure(
                state="normal"
            )

    def tile_displayed(self, position):
        tile = self.puzzle.get_tile(position)
        colorConvert = cv2.cvtColor(tile.image, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(colorConvert)
        draw = ImageDraw.Draw(image)
        width, height = image.size

        if self.controller._is_correct(position):
            x = width - 25
            y = 10
            draw.line(
                [
                    (x, y + 8),
                    (x + 6, y + 14),
                    (x + 17, y)
                ],
                fill="#33CD33",
                width=4
            )

        if (
            self.controller.hint_position == position
        ):
            radius = min(width, height) // 4
            x = width // 2
            y = height // 2
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline="#2867C5", width=4)

        photo = ImageTk.PhotoImage(image)
        self.display_images.append(photo)
        return photo

    def update_original_image(self, original_image_label):
        hint_position = self.controller.hint_position
        if hint_position is None:
            original_image_label.configure(image=self.puzzle.get_photoimage())
            self.original_display_image = (self.puzzle.get_photoimage())
            return
        #tiles that were given as hint
        hinted_tile = self.puzzle.get_tile(hint_position)
        # check home position of the tiles
        home_position = (self.controller._home_position.get(id(hinted_tile)))
        if home_position is None:
            return

        # Convert original image
        rgb_image = cv2.cvtColor(self.puzzle.image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb_image)
        draw = ImageDraw.Draw(image)

        # Maintaing size of tiles
        tile_width = (image.width // self.puzzle.grid_size)
        tile_height = (image.height // self.puzzle.grid_size)
        home_row, home_col = home_position
        x = (home_col * tile_width + tile_width // 2)
        y = (home_row * tile_height + tile_height // 2 )
        radius = min(tile_width, tile_height) // 4

        draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline="#0066FF", width=4)

        self.original_display_image = (ImageTk.PhotoImage(image))

        original_image_label.configure(image=self.original_display_image)

    def check_completion(self, was_locked):
        if (
            not was_locked
            and self.controller.locked
            and self.controller.tiles_incorrect() == 0
        ):

            messagebox.showinfo(
                "Game Completed",
                "Congratulations! You figured it out!"
            )