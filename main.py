import tkinter as tk
from tkinter import messagebox

from db.repository import Repository
from window.base import BaseWindow
from window.test import Test
from window.tree import Tree


class DigitalTwin(tk.Tk, BaseWindow):
    def __init__(self, module: Repository, w=400, h=300,
                 test_class=Test, w_test=300, h_test=400,
                 tree_class=Tree, w_tree=300, h_tree=400):
        super().__init__()
        self.title("Цифровой двойник студента")
        self.resizable(False, False)
        self.center_window(self, w, h)
        self.module = module

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.start_test_btn = tk.Button(self, text="Начать тестирование", command=self.start_test_action)
        self.start_test_btn.grid(row=1, column=1, pady=10)
        self.test_class = test_class
        self.w_test = w_test
        self.h_test = h_test

        self.show_tree_btn = tk.Button(self, text="Показать дерево результатов", command=self.show_tree_action)
        self.show_tree_btn.grid(row=2, column=1, pady=10)
        self.tree_class = tree_class
        self.w_tree = w_tree
        self.h_tree = h_tree

        self.exit_btn = tk.Button(self, text="Выйти", command=self.exit_action)
        self.exit_btn.grid(row=3, column=1, pady=10)

    def start_test_action(self):
        self.withdraw()
        test_window = self.test_class(self, self.module, self.w_test, self.h_test)
        test_window.show()

    def show_tree_action(self):
        self.withdraw()
        tree_window = self.tree_class(self, self.module, self.w_test, self.h_test)
        tree_window.show()

    def show_main(self):
        self.deiconify()

    def exit_action(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.destroy()

    def quit(self):
        self.exit_action()


if __name__ == "__main__":
    root = DigitalTwin(
        Repository(init_database=True),
        400, 300,
        Test, 300, 340,
        Tree, 300, 400)
    root.mainloop()
