import tkinter as tk

from .base import ChildWindow


class QuestionsWindow(ChildWindow):
    def __init__(self, parent, questions, w=300, h=400):
        super().__init__(parent, w, h)
        self.questions = questions
        self.index = 0
        self.current_q = self.questions[self.index]
        self.type = self.current_q.type
        self.option = tk.IntVar(value=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.timer = tk.Label(self, text="90")
        self.timer.grid(row=1, column=1, columnspan=2, pady=20)

        self.title_label = tk.Label(self)
        self.title_label.grid(row=2, column=1, columnspan=2, pady=10)

        self.text_label = tk.Label(self)
        self.text_label.grid(row=3, column=1, columnspan=2, pady=10)

        self.first_option = tk.Radiobutton(self,  variable=self.option, value=1)
        self.first_option.grid(row=4, column=1, columnspan=2, pady=10)
        self.second_option = tk.Radiobutton(self,  variable=self.option, value=2)
        self.second_option.grid(row=5, column=1, columnspan=2, pady=10)
        self.third_option = tk.Radiobutton(self,  variable=self.option, value=3)
        self.third_option.grid(row=6, column=1, columnspan=2, pady=10)

        self.next_q_btn = tk.Button(self, command=self.__next_q)
        self.next_q_btn.grid(row=7, column=2, pady=10)

        self.__update_q()

    def __update_width(self):
        self.update_idletasks()
        new_w = max(self.text_label.winfo_reqwidth(), self.first_option.winfo_reqwidth(),
                    self.second_option.winfo_reqwidth(), self.third_option.winfo_reqwidth()) + 50
        self.center_window(self, new_w if new_w > 300 else 300, 400)

    def __increment_index(self):
        if self.index < 2:
            self.index += 1
            self.current_q = self.questions[self.index]

    def __update_q(self):
        self.title_label.config(text=f"№ {self.index + 1}\tТип: {self.type}")
        self.text_label.config(text=self.current_q.text)
        self.first_option.config(text=self.current_q.options[1])
        self.second_option.config(text=self.current_q.options[2])
        self.third_option.config(text=self.current_q.options[3])
        if self.index < 2:
            self.next_q_btn.config(text="Следующий вопрос")
        else:
            self.next_q_btn.config(text="Закончить тестирование", command=self.return_to_main_to_main)
        self.__update_width()

    def __next_q(self):
        self.__increment_index()
        self.__update_q()
