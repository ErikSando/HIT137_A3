# Module for easily creating menus

import tkinter as tk

class MenuElem:
    # Take in the tk object and any layout arguments the user wants
    def __init__(self, tk_object: tk.Misc, show_type = "pack", visible = True, **layout_args):
        self.tk_object = tk_object
        self.show_type = show_type
        self.visible = visible
        self.layout_args = layout_args

        self.show_funcs = {
            "pack": self.pack,
            "grid": self.grid,
            "place": self.place
        }
         
        self.hide_funcs = {
            "pack": self.undo_pack,
            "grid": self.undo_grid,
            "place": self.undo_place
        }

    # Functions for showing/hiding
    def pack(self):
        self.tk_object.pack(**self.layout_args)

    def grid(self):
        self.tk_object.grid(**self.layout_args)

    def place(self):
        self.tk_object.place(**self.layout_args)

    def undo_pack(self):
        self.tk_object.pack_forget()

    def undo_grid(self):
        self.tk_object.grid_forget()

    def undo_place(self):
        self.tk_object.place_forget()

    def show(self):
        # Call a function to show the element depending on which layout manager is chosen
        self.show_funcs[self.show_type]()

    def hide(self):
        # Call a function to hide the element depending on which layout manager is chosen
        self.hide_funcs[self.show_type]()

    def toggle(self):
        self.visible = not self.visible

class Menu:
    def __init__(self, tk_root: tk.Tk, elements: list[MenuElem], visible = False, title = ""):
        self.elements = elements
        self.visible = visible
        self.title = title
        self.tk_root = tk_root

        # If initially set to visible, show the menu
        if self.visible:
            self.show()

    def add(self, *elements):
        for element in elements:
            self.elements.append(element)

            # If the menu is not visible, hide each element as it is added
            if not self.visible:
                element.hide()

    def remove(self, *elements):
        for element in elements:
            element.hide()
            self.elements.remove(element)

    def show(self):
        self.visible = True

        for element in self.elements:
            if not element.visible: # Don't show elements that are set as not visible
                continue

            element.show()

        if self.title and self.tk_window:
            self.tk_window.title(self.title)

    def hide(self):
        self.visible = False

        for element in self.elements:
            element.hide()

    def toggle(self):
        if self.visible:
            self.hide()

        else:
            self.show()

    def refresh(self):
        if not self.visible:
            return print("Cannot refresh menu that isn't visible")

        for element in self.elements:
            element.hide()

            if element.visible:
                element.show()
