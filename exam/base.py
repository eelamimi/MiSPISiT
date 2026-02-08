import tkinter


class BaseWindow:
    def center_window(self, window, w, h):
        x = (window.winfo_screenwidth() - w) // 2
        y = (window.winfo_screenheight() - h) // 2
        window.geometry(f"{w}x{h}+{x}+{y}")


class ChildWindow(tkinter.Toplevel, BaseWindow):
    def __init__(self, parent, w, h):
        super().__init__()
        self.parent = parent
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
