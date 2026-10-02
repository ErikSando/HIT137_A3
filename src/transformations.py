import cv2

from puzzle import Puzzle

class TransformationInfo:
    def __init__(self, puzzle: Puzzle, positions: list[tuple[int, int]], n_rotations: int = 1):
        self.puzzle = puzzle
        self.positions = positions
        self.n_rotations = n_rotations

class BaseTransformation:
    def apply(self, t_info: TransformationInfo):
        pass

class Swap(BaseTransformation):
    def apply(self, t_info: TransformationInfo):
        t_info.puzzle.swap_tiles(t_info.positions[0], t_info.positions[1])

class HorizontalFlip(BaseTransformation):
    def apply(self, t_info: TransformationInfo):
        tile = t_info.puzzle.get_tile(t_info.positions[0])
        tile.set_image(cv2.flip(tile.image, 1))

class VerticalFlip(BaseTransformation):
    def apply(self, t_info: TransformationInfo):
        tile = t_info.puzzle.get_tile(t_info.positions[0])
        tile.set_image(cv2.flip(tile.image, 0))

class Rotate(BaseTransformation):
    def apply(self, t_info: TransformationInfo):
        tile = t_info.puzzle.get_tile(t_info.positions[0])

        for _ in range(t_info.n_rotations):
            tile.set_image(cv2.rotate(tile.image, cv2.ROTATE_90_CLOCKWISE))