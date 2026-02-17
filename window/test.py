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
        self.difficulty = tk.StringVar(value='1')

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
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
        self.metric_combobox.bind('<<ComboboxSelected>>', self.__on_combobox_selected_update_difficulties)

        self.difficulty_label = ttk.Label(self, text="Сложность:", anchor='e')
        self.difficulty_label.grid(row=5, column=1, pady=10, padx=5, sticky='ew')
        self.difficulty_combobox = ttk.Combobox(self, textvariable=self.difficulty,
                                                values=self.difficulties_by_metric[self.metric.get()], state='readonly',
                                                width=17)
        self.difficulty_combobox.grid(row=5, column=2, pady=10, padx=5, sticky='ew')

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
        questions = self.module.generate_test(self.metric.get(), int(self.difficulty.get()))
        questions_window = QuestionsWindow(self, questions, 300, 650)
        questions_window.show()

    def save_results(self, result):
        student_name = self.student_entry.get().strip()
        student_id = self.module.get_student_id_by_name(student_name)
        if student_id is None or student_id == -1:
            student_id = self.module.save_student(student_name)

        full_section = f"РД {self.section_entry.get()}.{self.subsection_entry.get()}."

        pol = chl = umn = pol_c = chl_c = umn_c = 0
        metric = self.metric.get()
        if metric == 'POL':
            pol = result
            pol_c = int(self.difficulty.get())
        elif metric == 'CHL':
            chl = result
            chl_c = int(self.difficulty.get())
        else:
            umn = result
            umn_c = int(self.difficulty.get())
        self.module.save_results(student_id, full_section, pol_c, chl_c, umn_c, pol, chl, umn)

    def __validate_entries(self):
        if not self.student_entry.get().strip().isalpha():
            raise ValueError("Некорректно введена фамилия")
        if Test.__section_check(self.section_entry.get().strip()):
            raise ValueError("Некорректно введён раздел, используйте числа")
        if Test.__section_check(self.subsection_entry.get().strip()):
            raise ValueError("Некорректно введён подраздел, используйте числа")

    def __on_combobox_selected_update_difficulties(self, *args):
        self.difficulty_combobox.config(values=self.difficulties_by_metric[self.metric.get()])

    @staticmethod
    def __section_check(s):
        return s == "" or not all(c.isdigit() for c in s)

    def show_main(self):
        self.deiconify()
