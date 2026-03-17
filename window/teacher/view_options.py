import tkinter as tk

from window.child import ChildWindow


class ViewOptionsWindow(ChildWindow):
    def __init__(self, parent, text, options, answer):
        super().__init__(parent, 400, 300, True)
        self.title("Варианты ответов")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=0)
        self.grid_rowconfigure(5, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        tk.Label(self, text=f"Вопрос: {text}", wraplength=375,
                 font=('Arial', 10, 'bold')).grid(row=1, column=1, pady=10)

        frame = tk.Frame(self)
        frame.grid(row=2, column=1, sticky="nsew", padx=10)
        frame.grid_columnconfigure(0, weight=1)
        for i, (key, value) in enumerate(options.items()):
            tk.Label(frame, text=f"{key}. {value}", wraplength=375,
                     justify=tk.LEFT).grid(row=i, column=0, sticky="w", pady=2)

        tk.Label(self, text=f"Правильный ответ: {answer}",
                 font=('Arial', 10, 'bold')).grid(row=3, column=1, pady=10)
        tk.Button(self, text="Закрыть", command=self.close_menu).grid(row=4, column=1, pady=10)
