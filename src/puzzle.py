import cv2
import tkinter as tk
import random
from PIL import Image, ImageTk
from tile import Tile
from transformations import Rotate, HorizontalFlip, VerticalFlip

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
        self.tw = int(self.w / self.grid_size)
        self.th = int(self.h / self.grid_size)

        self.tiles = []
        self.initial_orientations = {}

        transformations = [
            Rotate(90), Rotate(180), Rotate(270),
            # duplicated so each type of transformation has a 1/3 chance of being picked, there's probably a better approach
            HorizontalFlip(), HorizontalFlip(), HorizontalFlip(),
            VerticalFlip(), VerticalFlip(), VerticalFlip()
        ]

        for i in range(self.grid_size):
            self.tiles.append([])

            for j in range(self.grid_size):
                tile = Tile(self.image[self.th * i : self.th * (i + 1), self.tw * j : self.tw * (j + 1)]) # crop the image
                t = random.choice(transformations) # random transformation
                t.apply(tile)
                self.tiles[i].append(tile)

        # swap 5 random tiles, placeholder for now, probably should make a setting for this

        indices = [ i for i in range(self.grid_size) ]

        for i in range(5):
            rows = indices.copy()
            cols = indices.copy()

            r1, c1 = random.choice(rows), random.choice(cols)

            rows.pop(r1)
            cols.pop(c1)

            r2, c2 = random.choice(rows), random.choice(cols)

            self.swap_tiles((r1, c1), (r2, c2))

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