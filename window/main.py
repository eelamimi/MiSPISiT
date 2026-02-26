import tkinter as tk
from tkinter import messagebox

from window.base import BaseWindow


class MainWindow(tk.Tk, BaseWindow):
    def __init__(self, w, h):
        super().__init__()
        self.resizable(False, False)
        self.center_window(self, w, h)
        self.protocol("WM_DELETE_WINDOW", self.exit_action)

    def show_main(self):
        self.deiconify()

    def exit_action(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.destroy()

    def quit(self):
        self.exit_action()