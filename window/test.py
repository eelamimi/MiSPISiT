import tkinter as tk
from tkinter import ttk, messagebox

from .base import ChildWindow
from diagnostic_module.tree import DiagnosticModuleTree
from .questions_window import QuestionsWindow


class Test(ChildWindow):
    def __init__(self, parent, module: DiagnosticModuleTree, w, h):
        super().__init__(parent, w, h)
        self.title("Тестирование")
        self.module = module

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.student_label = ttk.Label(self, text="Фамилия студента:", anchor='e')
        self.student_label.grid(row=1, column=1, pady=10, padx=5, sticky='ew')
        self.student_entry = ttk.Entry(self)
        self.student_entry.grid(row=1, column=2, pady=10, padx=5, sticky='ew')

        self.result_label = ttk.Label(self, text="Итоговый?", anchor='e')
        self.result_label.grid(row=2, column=1, pady=10, padx=5, sticky='ew')
        self.is_result_var = tk.StringVar(value="нет")  # переменная для хранения выбора
        self.yes_radio = ttk.Radiobutton(self, text="да", variable=self.is_result_var, value="да"
                                         , command=self.__lock_section)
        self.yes_radio.grid(row=2, column=2, pady=10, padx=(5, 2), sticky='w')
        self.no_radio = ttk.Radiobutton(self, text="нет", variable=self.is_result_var, value="нет"
                                        , command=self.__unlock_section)
        self.no_radio.grid(row=2, column=2, pady=10, padx=(2, 5), sticky='e')

        self.section_label = ttk.Label(self, text="Номер раздела:", anchor='e')
        self.section_label.grid(row=3, column=1, pady=10, padx=5, sticky='ew')
        self.section_entry = ttk.Entry(self)
        self.section_entry.grid(row=3, column=2, pady=10, padx=5, sticky='ew')

        self.subsection_label = ttk.Label(self, text="Номер подраздела:", anchor='e')
        self.subsection_label.grid(row=4, column=1, pady=10, padx=5, sticky='ew')
        self.subsection_entry = ttk.Entry(self)
        self.subsection_entry.grid(row=4, column=2, pady=10, padx=5, sticky='ew')

        self.complexity_label = ttk.Label(self, text="Сложность:", anchor='e')
        self.complexity_label.grid(row=5, column=1, pady=10, padx=5, sticky='ew')
        self.complexity_entry = ttk.Entry(self)
        self.complexity_entry.grid(row=5, column=2, pady=10, padx=5, sticky='ew')

        self.metric_label = ttk.Label(self, text="Метрика:", anchor='e')
        self.metric_label.grid(row=6, column=1, pady=10, padx=5, sticky='ew')
        self.metric_combobox = ttk.Combobox(self, values=['POL', 'CHL', 'UMN'], state='readonly', width=17)
        self.metric_combobox.set('POL')
        self.metric_combobox.grid(row=6, column=2, pady=10, padx=5, sticky='ew')

        self.start_test_button = tk.Button(self, text="Начать тестирование", command=self.start_test_action)
        self.start_test_button.grid(row=7, column=1, columnspan=2, pady=(20, 0))

        self.exit_button = tk.Button(self, text="Назад", command=self.return_to_main)
        self.exit_button.grid(row=8, column=1, columnspan=2, pady=10)

    def start_test_action(self):
        result_of_validation, message, values = self.__validate_entries()
        if not result_of_validation:
            messagebox.showerror("Ошибка", message)
            return
        self.withdraw()
        questions = self.module.generate_test(values[-1])
        questions_window = QuestionsWindow(self, questions, 300, 650)
        questions_window.show()

    def save_results(self, result, metric):
        student_name = self.student_entry.get().strip()
        student_id = self.module.get_student_id_by_name(student_name)
        if student_id is None or student_id == -1:
            student_id = self.module.save_student(student_name)

        if self.is_result_var == 'да':
            full_section = 'Итоговый'
        else:
            full_section = "РД " + self.section_entry.get() + '.' + self.subsection_entry.get() + '.'

        pol = chl = umn = 0
        if metric == 'POL':
            pol = result
        elif metric == 'CHL':
            chl = result
        else:
            umn = result
        self.module.save_results(student_id, full_section, int(self.complexity_entry.get()), pol, chl, umn)

    def __validate_entries(self) -> tuple[bool, str, list]:
        values = list()
        message = "Некорректно введена фамилия"
        try:
            if not self.student_entry.get().strip().isalpha():
                raise ValueError()
            message = "Некорректно введён раздел, используйте числа"
            raw_section = self.section_entry.get()
            if raw_section == "":
                raise ValueError()
            values.append(int(raw_section))
            message = "Некорректно введён подраздел, используйте числа"
            raw_subsection = self.subsection_entry.get()
            if raw_subsection == "":
                raise ValueError()
            values.append(int(raw_subsection))
            message = "Некорректно введена сложность, используйте числа"
            raw_complexity = self.complexity_entry.get()
            if raw_complexity == "":
                raise ValueError()
            values.append(complexity := int(raw_complexity))
            if complexity not in (complexities := self.module.get_complexities()[metric := self.metric_combobox.get()]):
                message = f"Для метрики {metric} сложности {complexity} нет. Есть сложности: {', '.join(map(str, complexities))}"
                raise ValueError()
            values.append(metric)
            return True, "", values
        except ValueError:
            return False, message, []

    def __lock_section(self):
        self.section_entry.config(state='disabled')
        self.subsection_entry.config(state='disabled')

    def __unlock_section(self):
        self.section_entry.config(state='normal')
        self.subsection_entry.config(state='normal')

    def show_main(self):
        self.deiconify()
