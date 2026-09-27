import cv2
import tkinter as tk
from PIL import Image, ImageTk

# An indivial tile in a tiled image puzzle
class Tile:
    def __init__(self, cv_image):
        self.set_image(cv_image)

    def set_image(self, cv_image):
        self.image = cv_image
        self.make_photoimage()

    # construct a PhotoImage from the OpenCV image to display with tkinter
    def make_photoimage(self):
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(rgb))

    def get_photoimage(self) -> tk.PhotoImage:
        return self.tk_image
