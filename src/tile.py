import cv2
import tkinter as tk
from PIL import Image, ImageTk

# An indivial tile in a tiled image puzzle
class Tile:
    def __init__(self, cv_image):
        self.image = cv_image
        self.make_photoimage()

    # construct a PhotoImage from the OpenCV image to display with tkinter
    def make_photoimage(self):
        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(rgb))

    def get_photoimage(self) -> tk.PhotoImage:
        return self.tk_image

    # # rotate by a multiple of 90 degrees
    # def rotate(self, n_rotations: int):
    #     for _ in range(n_rotations):
    #         self.image = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)

    #     self.make_photoimage()

    # # it might be better to make the transformations into seperate classes
    # # and perhaps have a .transform() function here that takes in an instance of a transformation class as an argument and applies it

    # # flip horizontally
    # def flip_hori(self):
    #     self.image = cv2.flip(self.image, 1)
    #     self.make_photoimage()

    # # flip vertically
    # def flip_vert(self):
    #     self.image = cv2.flip(self.image, 0)
    #     self.make_photoimage()