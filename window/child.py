import tkinter as tk

from window.base import BaseWindow


class ChildWindow(tk.Toplevel, BaseWindow):
    def __init__(self, parent, w, h):
        super().__init__()
        self.parent = parent
        self.resizable(False, False)
        self.center_window(self, w, h)
        self.protocol("WM_DELETE_WINDOW", self.exit_action)

    def show(self):
        self.grab_set()
        self.focus_set()

    def return_to_main(self):
        self.destroy()
        self.parent.show_main()

    def exit_action(self):
        self.destroy()
        self.parent.show_main()
