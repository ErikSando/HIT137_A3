import os
import sys
from pathlib import Path

# working directory needs to the project folder
root = Path(__file__).resolve().parent.parent
os.chdir(root)

# this prevents imports from failing due to the change in working directory
sys.path.insert(0, str(root / "src"))

from app import App

def main():
    app = App("Image Puzzle Game", 1100, 720)
    app.start()

if __name__ == "__main__":
    main()
