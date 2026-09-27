import cv2
from tile import Tile

class BaseTransformation:
    def transform(self, tile: Tile):
        pass

# Swap is handled by the Puzzle class, pixel data doesnt need to be changed in a swap, only tile indexing is changed

class HorizontalFlip(BaseTransformation):
    def transform(self, tile: Tile):
        tile.image = cv2.flip(tile.image, 1)
        tile.make_photoimage()

class VerticalFlip(BaseTransformation):
    def transform(self, tile: Tile):
        tile.image = cv2.flip(tile.image, 0)
        tile.make_photoimage()

class Rotate(BaseTransformation):
    def transform(self, tile: Tile):
        tile.image = cv2.rotate(tile.image, cv2.ROTATE_90_CLOCKWISE)
        tile.make_photoimage()