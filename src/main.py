from app import *
from puzzle import *
from window import *

def main():
    window = Window("Game", 1100, 650)
    app = App(window)
    app.start()

if __name__ == "__main__":
    main()
