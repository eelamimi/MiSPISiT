import tkinter as tk
from tkinter import ttk

from .base import ChildWindow
from diagnostic_module.tree import DiagnosticModuleTree
from .map import MapWindow


class Tree(ChildWindow):
    def __init__(self, parent, module: DiagnosticModuleTree, h, w):
        super().__init__(parent, h, w)
        self.title("Дерево результатов")
        self.module = module

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.student_label = ttk.Label(self, text="Студент:", anchor='e')
        self.student_label.grid(row=1, column=1, pady=10, padx=5, sticky='ew')
        students = self.module.get_all_students_have_final()
        self.student_combobox = ttk.Combobox(self, values=students, state='readonly', width=17)
        self.student_combobox.set(students[0])
        self.student_combobox.grid(row=1, column=2, pady=10, padx=5, sticky='ew')

        self.start_test_button = tk.Button(self, text="Построить дерево", command=self.create_tree)
        self.start_test_button.grid(row=2, column=1, columnspan=2, pady=(20, 0))

        self.exit_button = tk.Button(self, text="Назад", command=self.return_to_main)
        self.exit_button.grid(row=3, column=1, columnspan=2, pady=10)

    def create_tree(self):
        student_id = self.module.get_student_id_by_name(self.student_combobox.get())
        map_window = MapWindow(self, self.module.get_results_by_student_id(student_id))
        map_window.show()
        # self.module.plot_results_tree(self.module.create_results_tree(student_id), student_id)

    def show_main(self):
        self.deiconify()