class BaseWindow:
    def center_window(self, window, w, h):
        x = (window.winfo_screenwidth() - w) // 2
        y = (window.winfo_screenheight() - h) // 2
        window.geometry(f"{w}x{h}+{x}+{y}")
