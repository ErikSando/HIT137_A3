import cv2
from tile import Tile

class BaseTransformation:
    def apply(self, tile: Tile):
        pass

# Swap is handled by the Puzzle class, pixel data doesnt need to be changed in a swap, only tile indexing is changed

class HorizontalFlip(BaseTransformation):
    def apply(self, tile: Tile):
        tile.set_image(cv2.flip(tile.image, 1))

class VerticalFlip(BaseTransformation):
    def apply(self, tile: Tile):
        tile.set_image(cv2.flip(tile.image, 0))

class Rotate(BaseTransformation):
    def __init__(self, n_rotations: int = 1):
        self.n_rotations = n_rotations

    def apply(self, tile: Tile):
        for i in range(self.n_rotations):
            tile.set_image(cv2.rotate(tile.image, cv2.ROTATE_90_CLOCKWISE))