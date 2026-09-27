import cv2
import tkinter as tk
from PIL import Image, ImageTk
from tile import *

# Handles resizing, tiling and transformations on images to create puzzles
class Puzzle:
    def __init__(self, source: str, grid_size: int = 3, max_size: int = 400):
        raw_image = cv2.imread(source)

        if raw_image is None:
            raise RuntimeError(f"could not open image: '{source}'")

        w, h = raw_image.shape[1], raw_image.shape[0]
        max_dim = max(w, h)
        scale = max_size / max_dim

        self.image = cv2.resize(raw_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        self.w, self.h = self.image.shape[1], self.image.shape[0]

        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(rgb))

        self.grid_size = grid_size
        self.make_tiles()

    def make_tiles(self, grid_size: int = None):
        if grid_size is not None:
            self.grid_size = grid_size

        # width and height of individual tiles
        tw = int(self.w / self.grid_size)
        th = int(self.h / self.grid_size)

        self.tiles = []

        for i in range(self.grid_size):
            self.tiles.append([])

            for j in range(self.grid_size):
                tile = Tile(self.image[th * i : th * (i + 1), tw * j : tw * (j + 1)]) # crop the image
                # apply a transformation here, alternatively apply the transformation in the App class
                self.tiles[i].append(tile)

    def swap_tiles(self, x1: int, x2: int, y1: int, y2: int):
        temp = self.tiles[y1][x1]
        self.tiles[y1][x1] = self.tiles[y2][x2]
        self.tiles[y2][x2] = temp

    def get_photoimage(self) -> tk.PhotoImage:
        return self.tk_image

    def get_grid(self):
        pass