# HIT137_A3
  A desktop image puzzle game built with tkinter.
  The user selects an image, and it is made into a puzzle by dividing into a grid, and scrambling using horizontal/vertical flips, multiples of 90 degree rotations, and tile position swaps.
  To form an even grid, the image is cropped into a square (the largest square that can be formed in the centre of the image).
  The user can reshuffle the tiles using mouse controls and the shift key to reconstruct the original image. The controls are:
  * Left click: highlight a tile. If a second tile is left clicked while another is highlighted, the two tiles are swapped.
  * Right click: rotate a tile 90 degrees clockwise.
  * Shift + left click: horizontally flip a tile.

  Correct tiles are marked with a green tick in the top right corner.
  Additional features are:
  * Hints: a button to highlight an incorrect tile and it's correct position
  * Solve: a button that automatically solves the puzzle
  * Move counting: count the number of transformations (flip, rotate, swap) made by the player

### Dependencies

The packages used by the project are (excluding default Python packages):

  * NumPy
  * Pillow
  * OpenCV

  Install command (pip):

  ```
  pip install numpy Pillow opencv-python
  ```

### Usage

  Using launch.py:

  ```
  python launch.py
  ```

  Using main.py:

  ```
  python src/main.py
  ```

  Alternatively, open launch.py or main.py directly from a file explorer window. The app will adjust it's working directory to correctly access modules and the resource folder.