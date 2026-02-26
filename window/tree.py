import tkinter as tk
from tkinter import ttk

from window.child import ChildWindow
from db.repository import Repository
from window.map import MapWindow


class Tree(ChildWindow):
    def __init__(self, parent, module: Repository, h, w):
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
        students = self.module.get_all_students_have_result()
        self.student_combobox = ttk.Combobox(self, values=students, state='readonly', width=17)
        self.student_combobox.set(students[0])
        self.student_combobox.grid(row=1, column=2, pady=10, padx=5, sticky='ew')

        self.start_test_button = tk.Button(self, text="Построить дерево", command=self.create_tree)
        self.start_test_button.grid(row=2, column=1, columnspan=2, pady=(20, 0))

        self.exit_button = tk.Button(self, text="Назад", command=self.return_to_main)
        self.exit_button.grid(row=3, column=1, columnspan=2, pady=10)

    def create_tree(self):
        self.withdraw()
        student_name = self.student_combobox.get()
        student_id = self.module.get_student_id_by_name(student_name)
        map_window = MapWindow(self, self.module, student_name, self.module.get_results_by_student_id(student_id))
        map_window.show()

    def show_main(self):
        self.deiconify()
        