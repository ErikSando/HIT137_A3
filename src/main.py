from app import *
from puzzle import *
from window import *

def main():
    window = Window("Game", 800, 600)
    app = App(window)
    app.start()

if __name__ == "__main__":
    main()
