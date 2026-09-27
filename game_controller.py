"""
game_controller.py

GameController: coordinates a single round of play - moves, hints, solve
and completion state. It only talks to a PuzzleImage (class interaction),
and knows nothing about Tkinter, so the GUI layer stays a thin skin on
top of this.
"""

import random


class GameController:
    MAX_HINTS = 3

    def __init__(self, puzzle_image):
        self.puzzle = puzzle_image
        self.moves = 0
        self.hints_used = 0
        self.hint_tile_id = None
        self.selected_tile_id = None
        self.locked = False  # True once solved - no further puzzle input accepted

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def tiles_incorrect(self):
        return sum(1 for t in self.puzzle.tiles.values() if not t.is_correct())

    def hints_remaining(self):
        return self.MAX_HINTS - self.hints_used

    def tile_at(self, position):
        for tile in self.puzzle.tiles.values():
            if tile.position == position:
                return tile
        return None

    # ------------------------------------------------------------------
    # Player actions
    # ------------------------------------------------------------------
    def handle_left_click(self, position):
        """Select a tile; a second click on a different tile swaps them;
        clicking the same tile again deselects it."""
        if self.locked:
            return
        tile = self.tile_at(position)
        if tile is None:
            return  # off-grid / empty slot - ignore gracefully

        if self.selected_tile_id is None:
            self.selected_tile_id = tile.id
            return
        if self.selected_tile_id == tile.id:
            self.selected_tile_id = None  # deselect
            return

        other = self.puzzle.tiles[self.selected_tile_id]
        tile.position, other.position = other.position, tile.position
        self.selected_tile_id = None
        self._register_move()

    def handle_right_click(self, position):
        """Rotate the clicked tile 90 degrees clockwise."""
        if self.locked:
            return
        tile = self.tile_at(position)
        if tile is None:
            return
        tile.rotate(90)
        self.selected_tile_id = None
        self._register_move()

    def handle_shift_click(self, position):
        """Flip the clicked tile horizontally."""
        if self.locked:
            return
        tile = self.tile_at(position)
        if tile is None:
            return
        tile.flip("horizontal")
        self.selected_tile_id = None
        self._register_move()

    def use_hint(self):
        """Mark one incorrect tile; returns that Tile, or None if unavailable."""
        if self.locked or self.hints_used >= self.MAX_HINTS:
            return None
        incorrect = [t for t in self.puzzle.tiles.values() if not t.is_correct()]
        if not incorrect:
            return None
        tile = random.choice(incorrect)
        self.hints_used += 1
        self.hint_tile_id = tile.id
        return tile

    def solve(self):
        """Instantly solve the puzzle and clear moves/score."""
        self.puzzle.solve()
        self.moves = 0
        self.hints_used = 0
        self.hint_tile_id = None
        self.selected_tile_id = None
        self.locked = True

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _register_move(self):
        self.moves += 1
        self.hint_tile_id = None  # the hint circle disappears after the next move
        if self.puzzle.is_solved():
            self.locked = True
