import cv2
import tkinter as tk
from PIL import Image, ImageTk

from tile import Tile

# Handles resizing, tiling and transformations on images to create puzzles
class Puzzle:
    def __init__(self, source: str, grid_size: int, resize: int = 400):
        raw_image = cv2.imread(source)

        if raw_image is None:
            raise RuntimeError(f"could not open image: '{source}'")

        #Stores the grid size selected by user
        self.grid_size = grid_size 

        w, h = raw_image.shape[1], raw_image.shape[0]

        size = min(w, h)

        start_x = int((w - size) / 2)
        start_y = int((h - size) / 2)

        raw_image = raw_image[start_y : start_y + size, start_x : start_x + size]

        scale = resize / size

        self.image = cv2.resize(raw_image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

        self.w, self.h = self.image.shape[1], self.image.shape[0]
        # Divide image evenly by the grid size selected
        new_w = (self.w // self.grid_size) * self.grid_size 
        new_h = (self.h // self.grid_size) * self.grid_size
        self.image = self.image[:new_h, :new_w] 
        
        # Update dimensions
        self.w = self.image.shape[1] 
        self.h = self.image.shape[0]

        rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.tk_image = ImageTk.PhotoImage(Image.fromarray(rgb))

        # self.grid_size = grid_size --commented
        self.make_tiles()

    def make_tiles(self, grid_size: int = None):
        if grid_size is not None:
            self.grid_size = grid_size

        # width and height of individual tiles
        self.tw = int(self.w / self.grid_size)
        self.th = int(self.h / self.grid_size)

        self.tiles = []
        self.initial_orientations = {}

        for i in range(self.grid_size):
            self.tiles.append([])

            for j in range(self.grid_size):
                tile = Tile(self.image[self.th * i : self.th * (i + 1), self.tw * j : self.tw * (j + 1)]) # crop the image
                self.tiles[i].append(tile)

    def get_tile(self, pos: tuple[int, int]) -> Tile:
        r, c = pos

        assert r >= 0 and r < self.grid_size, "row number does not fit within the grid size"
        assert c >= 0 and c < self.grid_size, "column number does not fit within the grid size"

        return self.tiles[r][c]

    def swap_tiles(self, pos1: tuple[int, int], pos2: tuple[int, int]):
        tile1, tile2 = self.get_tile(pos1), self.get_tile(pos2) # checks if the positions are valid

        r1, c1 = pos1
        r2, c2 = pos2

        self.tiles[r1][c1], self.tiles[r2][c2] = tile2, tile1

    def reset_tiles(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.tiles[i][j] = Tile(self.image[self.th * i : self.th * (i + 1), self.tw * j : self.tw * (j + 1)])

    def get_photoimage(self) -> tk.PhotoImage:
        return self.tk_image

    def solve():
        pass

    def get_grid(self):
        pass