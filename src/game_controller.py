"""
game_controller.py

Adapted to the group's real Puzzle / Tile / transformations classes.

Two things had to be handled differently from a from-scratch design,
because of how those classes actually work:

1. Tile has no id, no home-position, and no orientation state - Puzzle
   just holds tiles in a plain 2D list, and HorizontalFlip / VerticalFlip /
   Rotate mutate a tile's pixels directly with nothing recording what was
   done. So THIS class keeps that bookkeeping itself: which tile object
   (by python id()) belongs in which slot, and its current rotation/flip
   state - tracked internally, not stored on Tile.

2. Puzzle only exposes swap_tiles() for moving tiles - there's no
   "rotate/flip this tile" method - so rotate/flip actions call
   HorizontalFlip / Rotate from transformations.py directly on the Tile
   object. Swap still goes entirely through Puzzle.swap_tiles(), so this
   class never touches tile pixel data for a swap.

*** REQUIRES two small additions to puzzle.py - see the bottom of this
file for exactly what to add and why. Without them this still runs, but
"tiles incorrect", hints, and win detection can't see the tiles' initial
scrambled orientation, and Solve has no way to rebuild the original
tiles - see NotImplementedError below. ***
"""

import random

from transformations import HorizontalFlip, Rotate
from puzzle import Puzzle

class GameController:
    MAX_HINTS = 3

    def __init__(self, puzzle: Puzzle):
        self.puzzle = puzzle
        self.moves = 0
        self.hints_used = 0
        self.hint_position = None      # (row, col) currently hinted, or None
        self.selected_position = None  # (row, col) currently selected, or None
        self.locked = False            # True once solved - no further input accepted

        self._home_position = {}       # id(tile) -> (row, col) it started in
        self._orientation = {}         # id(tile) -> {"rotation": 0/90/180/270, "flip_h": bool}
        self._reindex(puzzle.initial_orientations)

    # ------------------------------------------------------------------
    # Bookkeeping
    # ------------------------------------------------------------------
    def _reindex(self, seed_from):
        """(Re)build home-position/orientation tracking from the tiles
        currently sitting in puzzle.tiles - called on init and after solve().
        """
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
        """Translate puzzle.py's record of "what scramble transform did I
        apply here" into (rotation, flip_h) bookkeeping.

        A vertical flip and a horizontal-flip-plus-180-rotation look
        identical on screen (a property of the square's symmetry group),
        so they're stored the same way - that's what guarantees the player
        can always reach "solved" using only the two actions they're given
        (rotate 90 deg clockwise, flip horizontal).
        """
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

    def _is_correct(self, row, col):
        tile = self.puzzle.tiles[row][col]
        orient = self._orientation[id(tile)]
        return (
            self._home_position[id(tile)] == (row, col)
            and orient["rotation"] == 0
            and not orient["flip_h"]
        )

    def _valid(self, position):
        row, col = position
        n = self.puzzle.grid_size
        return 0 <= row < n and 0 <= col < n

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def tiles_incorrect(self):
        n = self.puzzle.grid_size
        return sum(1 for r in range(n) for c in range(n) if not self._is_correct(r, c))

    def hints_remaining(self):
        return self.MAX_HINTS - self.hints_used

    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def handle_left_click(self, position):
        """Select a tile; a second click on a different tile swaps them;
        clicking the same tile again deselects it."""
        if self.locked or not self._valid(position):
            return
        row, col = position

        if self.selected_position is None:
            self.selected_position = position
            return
        if self.selected_position == position:
            self.selected_position = None
            return

        sel_row, sel_col = self.selected_position
        # NOTE: Puzzle.swap_tiles has an unusual argument order -
        # (col_a, col_b, row_a, row_b), not two (row, col) pairs.
        self.puzzle.swap_tiles(sel_col, col, sel_row, row)
        self.selected_position = None
        self._register_move()

    def handle_right_click(self, position):
        """Rotate the clicked tile 90 degrees clockwise."""
        if self.locked or not self._valid(position):
            return
        row, col = position
        tile = self.puzzle.tiles[row][col]
        Rotate().transform(tile, 1)
        orient = self._orientation[id(tile)]
        orient["rotation"] = (orient["rotation"] + 90) % 360
        self.selected_position = None
        self._register_move()

    def handle_shift_click(self, position):
        """Flip the clicked tile horizontally."""
        if self.locked or not self._valid(position):
            return
        row, col = position
        tile = self.puzzle.tiles[row][col]
        HorizontalFlip().transform(tile)
        orient = self._orientation[id(tile)]
        orient["flip_h"] = not orient["flip_h"]
        self.selected_position = None
        self._register_move()

    def use_hint(self):
        """Mark one incorrect tile; returns its (row, col), or None."""
        if self.locked or self.hints_used >= self.MAX_HINTS:
            return None
        n = self.puzzle.grid_size
        incorrect = [(r, c) for r in range(n) for c in range(n) if not self._is_correct(r, c)]
        if not incorrect:
            return None
        position = random.choice(incorrect)
        self.hints_used += 1
        self.hint_position = position
        return position

    def solve(self):
        """Instantly solve the puzzle and clear moves/score."""
        self.puzzle.reset_tiles()
        self._reindex(seed_from=None)  # freshly rebuilt tiles are all correctly oriented
        self.moves = 0
        self.hints_used = 0
        self.hint_position = None
        self.selected_position = None
        self.locked = True

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _register_move(self):
        self.moves += 1
        self.hint_position = None  # the hint clears after the next move
        if self.tiles_incorrect() == 0:
            self.locked = True
