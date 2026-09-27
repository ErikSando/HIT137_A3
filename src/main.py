from app import App
from window import Window

def main():
    window = Window("Game", 1100, 650)
    app = App(window)
    app.start()

if __name__ == "__main__":
    main()
