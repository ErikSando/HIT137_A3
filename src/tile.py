import cv2
import tkinter as tk
from PIL import Image, ImageTk

# An indivial tile in a tiled image puzzle
class Tile:
    def __init__(self, cv_image):
        self.image = cv_image

        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb)
        self.tk_image = ImageTk.PhotoImage(pil_image)

    def get_image(self) -> tk.PhotoImage:
        return self.tk_image

    # rotate by a multiple of 90 degrees
    def rotate(n_rotations: int):
        pass

    # flip horizontally
    def flip_hori():
        pass

    # flip vertically
    def flip_vert():
        pass