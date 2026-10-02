import random
import numpy as np

from transformations import TransformationInfo, Swap, Rotate, HorizontalFlip
from puzzle import Puzzle

class GameController:
    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle

        self.moves = 0
        self.hints_used = 0
        self.hint_position = None      # (row, col) currently hinted, or None
        self.selected_position = None  # (row, col) currently selected, or None
        self.locked = False            # True once solved - no further input accepted

        self._home_position = {}       # id(tile) -> (row, col) it started in
        self._orientation = {}         # id(tile) -> {"rotation": 0/90/180/270, "flip_h": bool}
        self._original_img = {}      
        self._reindex(puzzle.initial_orientations)
        self._original_img_state()

        self.MAX_HINTS = 3

    # Bookkeeping
    def _reindex(self, seed_from):
        self._home_position = {}
        self._orientation = {}
        for row in range(self.puzzle.grid_size):
            for col in range(self.puzzle.grid_size):
                tile = self.puzzle.tiles[row][col]
                self._home_position[id(tile)] = (row, col)
                entry = seed_from.get((row, col)) if seed_from else None
                self._orientation[id(tile)] = self._decode_raw(entry)

    @staticmethod
    def _decode_raw(entry):
        # Translate puzzle.py's record of transforms into (rotation, flip_h) bookkeeping.
        if not entry:
            return {"rotation": 0, "flip_h": False}
        kind = entry.get("kind")
        if kind == "rotate":
            return {"rotation": (entry.get("n", 0) * 90) % 360, "flip_h": False}
        if kind == "flip_h":
            return {"rotation": 0, "flip_h": True}
        if kind == "flip_v":
            return {"rotation": 180, "flip_h": True}
        return {"rotation": 0, "flip_h": False}

    def _original_img_state(self):
        self._original_img = {}
        for row in range(self.puzzle.grid_size):
            for col in range(self.puzzle.grid_size):
                tile = self.puzzle.tiles[row][col]
                self._original_img[id(tile)] = tile.image.copy()

    def _is_correct(self, pos: tuple[int, int]):
        tile = self.puzzle.get_tile(pos)
        tile_id = id(tile)

        if self._home_position.get(tile_id) != pos:
            return False

        original_image = self._original_img.get(tile_id)
        if original_image is None:
            return False
        
        return np.array_equal(
            tile.image,
            original_image
        )

    def _valid(self, position: tuple[int, int]):
        row, col = position
        n = self.puzzle.grid_size
        return 0 <= row < n and 0 <= col < n

    def tiles_incorrect(self) -> int:
        n = 0

        for r in range(self.puzzle.grid_size):
            for c in range(self.puzzle.grid_size):
                if not self._is_correct((r, c)):
                    n += 1

        return n

    def hints_remaining(self) -> int:
        return self.MAX_HINTS - self.hints_used

    # Player actions

    def handle_left_click(self, position: tuple[int, int]):
        """Select a tile; a second click on a different tile swaps them;
        clicking the same tile again deselects it."""

        if self.locked or not self._valid(position):
            return

        if self.selected_position is None:
            self.selected_position = position
            return

        if self.selected_position == position:
            self.selected_position = None
            return

        t_info = TransformationInfo(self.puzzle, [position, self.selected_position])
        Swap().apply(t_info)

        self.selected_position = None
        self._register_move()

    def handle_right_click(self, position: tuple[int, int]):
        """Rotate the clicked tile 90 degrees clockwise."""

        if self.locked or not self._valid(position):
            return

        t_info = TransformationInfo(self.puzzle, [position])
        Rotate().apply(t_info)

        row, col = position
        tile = self.puzzle.tiles[row][col]
        orient = self._orientation[id(tile)]
        orient["rotation"] = (orient["rotation"] + 90) % 360

        self.selected_position = None
        self._register_move()

    def handle_shift_click(self, position: tuple[int, int]):
        """Flip the clicked tile horizontally."""

        if self.locked or not self._valid(position):
            return

        t_info = TransformationInfo(self.puzzle, [position])
        HorizontalFlip().apply(t_info)

        row, col = position
        tile = self.puzzle.tiles[row][col]
        orient = self._orientation[id(tile)]
        orient["flip_h"] = not orient["flip_h"]

        self.selected_position = None
        self._register_move()

    def use_hint(self):
        """Mark one incorrect tile; returns its (row, col), or None."""

        if self.locked or self.hints_used >= self.MAX_HINTS:
            return None

        incorrect_tiles = []

        for r in range(self.puzzle.grid_size):
            for c in range(self.puzzle.grid_size):
                if not self._is_correct((r, c)):
                    incorrect_tiles.append((r, c))

        if not incorrect_tiles:
            return None

        position = random.choice(incorrect_tiles)

        self.hints_used += 1
        self.hint_position = position

        return position

    def solve(self):
        """Instantly solve the puzzle and clear moves/score."""

        self.puzzle.reset_tiles()
        self._reindex(seed_from=None)  # freshly rebuilt tiles are all correctly oriented
        self._original_img_state()
        self.moves = 0
        self.hints_used = 0
        self.hint_position = None
        self.selected_position = None
        self.locked = True

    def _register_move(self):
        self.moves += 1
        self.hint_position = None  # the hint clears after the next move

        if self.tiles_incorrect() == 0:
            self.locked = True