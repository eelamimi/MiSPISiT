import tkinter as tk

from window.base import BaseWindow


class ChildWindow(tk.Toplevel, BaseWindow):
    def __init__(self, parent, w, h, is_modal=False):
        super().__init__()
        self.parent = parent
        self.resizable(False, False)
        self.center_window(self, w, h)
        self.protocol("WM_DELETE_WINDOW", self.exit_action)

        if is_modal:
            self.transient(self.parent)

    def show(self):
        self.grab_set()
        self.focus_set()

    def return_to_main(self):
        self.destroy()
        self.parent.show_main()

    def exit_action(self):
        self.destroy()
        self.parent.show_main()

    def close_menu(self):
        self.destroy()


class ChildChildWindow(ChildWindow):
    def __init__(self, parent_of_parent, parent, w, h, is_modal=False):
        super().__init__(parent, w, h, is_modal)
        self.parent_of_parent = parent_of_parent

    def return_to_main(self):
        self.destroy()
        self.parent.destroy()
        self.parent_of_parent.show_main()

    def exit_action(self):
        self.return_to_main()
