import tkinter as tk
from tkinter import ttk, messagebox

from diagnostic_module.tree import DiagnosticModuleTree
from .base import ChildWindow
from .questions import QuestionsWindow


class Test(ChildWindow):
    def __init__(self, parent, module: DiagnosticModuleTree, w, h):
        super().__init__(parent, w, h)
        self.title("Тестирование")
        self.module = module
        self.difficulties_by_metric = module.get_difficulties()
        metrics = ['POL', 'CHL', 'UMN']
        self.metric = tk.StringVar(value='POL')
        self.max_difficulty = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.student_label = ttk.Label(self, text="Фамилия студента:", anchor='e')
        self.student_label.grid(row=1, column=1, pady=10, padx=5, sticky='ew')
        self.student_entry = ttk.Entry(self)
        self.student_entry.grid(row=1, column=2, pady=10, padx=5, sticky='ew')

        self.section_label = ttk.Label(self, text="Номер раздела:", anchor='e')
        self.section_label.grid(row=2, column=1, pady=10, padx=5, sticky='ew')
        self.section_entry = ttk.Entry(self)
        self.section_entry.grid(row=2, column=2, pady=10, padx=5, sticky='ew')

        self.subsection_label = ttk.Label(self, text="Номер подраздела:", anchor='e')
        self.subsection_label.grid(row=3, column=1, pady=10, padx=5, sticky='ew')
        self.subsection_entry = ttk.Entry(self)
        self.subsection_entry.grid(row=3, column=2, pady=10, padx=5, sticky='ew')

        self.metric_label = ttk.Label(self, text="Метрика:", anchor='e')
        self.metric_label.grid(row=4, column=1, pady=10, padx=5, sticky='ew')
        self.metric_combobox = ttk.Combobox(self, textvariable=self.metric, values=metrics, state='readonly', width=17)
        self.metric_combobox.grid(row=4, column=2, pady=10, padx=5, sticky='ew')

        self.start_test_button = tk.Button(self, text="Начать тестирование", command=self.start_test_action)
        self.start_test_button.grid(row=6, column=1, columnspan=2, pady=(20, 0))

        self.exit_button = tk.Button(self, text="Назад", command=self.return_to_main)
        self.exit_button.grid(row=7, column=1, columnspan=2, pady=10)

    def start_test_action(self):
        try:
            self.__validate_entries()
        except ValueError as e:
            messagebox.showerror("Ошибка", e)
            return
        self.withdraw()
        questions, self.max_difficulty = self.module.generate_test(self.metric.get())
        questions_window = QuestionsWindow(self, questions, self.max_difficulty, 300, 650)
        questions_window.show()

    def save_results(self, result):
        if self.max_difficulty == 0:
            raise SystemExit("Как")

        student_name = self.student_entry.get().strip()
        student_id = self.module.get_student_id_by_name(student_name)
        if student_id is None or student_id == -1:
            student_id = self.module.save_student(student_name)

        full_section = f"РД {self.section_entry.get()}.{self.subsection_entry.get()}."

        pol = chl = umn = pol_c = chl_c = umn_c = 0
        metric = self.metric.get()
        if metric == 'POL':
            pol = result
            pol_c = self.max_difficulty
        elif metric == 'CHL':
            chl = result
            chl_c = self.max_difficulty
        else:
            umn = result
            umn_c = self.max_difficulty
        self.module.save_results(student_id, full_section, pol_c, chl_c, umn_c, pol, chl, umn)

    def __validate_entries(self):
        if not self.student_entry.get().strip().isalpha():
            raise ValueError("Некорректно введена фамилия")
        if Test.__section_check(self.section_entry.get().strip()):
            raise ValueError("Некорректно введён раздел, используйте числа")
        if Test.__section_check(self.subsection_entry.get().strip()):
            raise ValueError("Некорректно введён подраздел, используйте числа")

    @staticmethod
    def __section_check(s):
        return s == "" or not all(c.isdigit() for c in s)

    def show_main(self):
        self.deiconify()
