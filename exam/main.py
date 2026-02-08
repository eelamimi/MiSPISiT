import tkinter as tk
from tkinter import font
from tkinter import messagebox

from base import BaseWindow
from questions import QuestionsRepository
from test_module import TestModule


class MainWindow(tk.Tk, BaseWindow):
    def __init__(self, w=400, h=300):
        super().__init__()
        self.title("Экзаменационное тестирование")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.exit_action)
        self.center_window(self, w, h)
        self.test_class = TestModule

        # Создаем шрифт размером 14 пикселей
        self.custom_font = font.Font(family="Helvetica", size=14)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.type_of_questions = tk.StringVar(value="POL")

        self.type_pol_radiobutton = tk.Radiobutton(
            self,
            text='POL',
            variable=self.type_of_questions,
            value="POL",
            font=self.custom_font
        )
        self.type_pol_radiobutton.grid(row=1, column=1, pady=10)

        self.type_chl_radiobutton = tk.Radiobutton(
            self,
            text='CHL',
            variable=self.type_of_questions,
            value="CHL",
            font=self.custom_font
        )
        self.type_chl_radiobutton.grid(row=1, column=2, pady=10)

        self.start_test_first_btn = tk.Button(
            self,
            text="Начать тестирование 1",
            command=self.start_test_first_action,
            font=self.custom_font
        )
        self.start_test_first_btn.grid(row=2, column=1, columnspan=2, pady=10)

        self.start_test_second_btn = tk.Button(
            self,
            text="Начать тестирование 2",
            command=self.start_test_second_action,
            font=self.custom_font
        )
        self.start_test_second_btn.grid(row=3, column=1, columnspan=2, pady=10)

        self.res_btn = tk.Button(
            self,
            text="Показать статистику",
            command=self.show_res,
            font=self.custom_font
        )
        self.res_btn.grid(row=4, column=1, columnspan=2, pady=10)

        self.exit_btn = tk.Button(
            self,
            text="Выйти",
            command=self.exit_action,
            font=self.custom_font
        )
        self.exit_btn.grid(row=5, column=1, columnspan=2, pady=10)

        self.results = {}
        self.repository = QuestionsRepository()

    def start_test_first_action(self):
        self.withdraw()
        questions = self.repository.get_questions_by_part_and_type(1, self.type_of_questions.get())
        test_window = self.test_class(self, questions, self.results, 1)
        test_window.show()

    def start_test_second_action(self):
        self.withdraw()
        questions = self.repository.get_questions_by_part_and_type(2, self.type_of_questions.get())
        test_window = self.test_class(self, questions, self.results, 2)
        test_window.show()

    def show_res(self):
        if 4 == len(self.results.keys()):
            msg = ""
            msg += f"POL 1 тест: {self.results['POL 1 тест']}\n"
            msg += f"CHL 1 тест: {self.results['CHL 1 тест']}\n\n"
            msg += f"POL 2 тест: {self.results['POL 2 тест']}\n"
            msg += f"CHL 2 тест: {self.results['CHL 2 тест']}\n\n"
            sum1 = self.results['POL 1 тест'] + self.results['CHL 1 тест']
            sum2 = self.results['POL 2 тест'] + self.results['CHL 2 тест']
            msg += f"1 тест (POL + CHL): {sum1}\n"
            msg += f"2 тест (POL + CHL): {sum2}\n\n"
            msg += f"Общий балл: {round((sum1 + sum2) / 2)}"
            messagebox.showinfo("Результаты", msg)
        else:
            messagebox.showerror("Результаты", "Ошибка\n\nВы должны пройти все 4 теста")

    def show_main(self):
        self.deiconify()

    def exit_action(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти?"):
            self.destroy()

    def quit(self):
        self.exit_action()


if __name__ == "__main__":
    root = MainWindow(400, 300)
    root.mainloop()
