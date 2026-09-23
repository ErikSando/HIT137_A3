import tkinter as tk

# Light wrapper for a tkinter window
class Window(tk.Tk):
    def __init__(self, title: str, width: int, height: int):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")

