import cv2
from tile import *

class BaseTransformation:
    def transform(self, tile: Tile):
        pass

class HorizontalFlip(BaseTransformation):
    def transform(self, tile: Tile):
        tile.image = cv2.flip(tile.image, 1)
        tile.make_photoimage()

class VerticalFlip(BaseTransformation):
    def transform(self, tile: Tile):
        tile.image = cv2.flip(tile.image, 0)
        tile.make_photoimage()

class Rotate(BaseTransformation):
    def transform(self, tile: Tile, n_rotations: int):
        for _ in range(n_rotations):
            tile.image = cv2.rotate(tile.image, cv2.ROTATE_90_CLOCKWISE)

        tile.make_photoimage()