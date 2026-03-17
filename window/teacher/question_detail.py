import tkinter as tk
from tkinter import ttk, messagebox

from window.child import ChildWindow


class QuestionDetailWindow(ChildWindow):
    def __init__(self, parent, repository, question_id):
        self.h = 500
        self.w = 700
        self.w_right_frame = 150
        super().__init__(parent, self.w, self.h, True)
        self.repository = repository
        self.question_id = question_id
        if question_id:
            self.title_name = "Редактирование вопроса"
            self.action_button_text = "Изменить"
            self.exit_message = "Вопрос изменён"
            question = self.repository.get_question_by_id(question_id)
            self.question_text = tk.StringVar(value=question.text)
            self.correct_answer = tk.StringVar(value=str(question.answer))
            self.difficulty = tk.StringVar(value=str(question.difficulty))
            self.question_type = tk.StringVar(value=question.type)
            self.options = question.options
        else:
            self.title_name = "Добавление вопроса"
            self.action_button_text = "Сохранить"
            self.exit_message = "Вопрос сохранён"
            self.question_text = tk.StringVar()
            self.correct_answer = tk.StringVar()
            self.difficulty = tk.StringVar()
            self.question_type = tk.StringVar()
            self.options = dict()
        self.title(self.title_name)

        self.grid_columnconfigure(0, weight=0, minsize=0)
        self.grid_columnconfigure(1, weight=0, minsize=self.w - self.w_right_frame)
        self.grid_columnconfigure(2, weight=0, minsize=self.w_right_frame)
        self.grid_columnconfigure(3, weight=1, minsize=0)
        self.grid_rowconfigure(0, weight=0, minsize=0)
        self.grid_rowconfigure(1, weight=1, minsize=self.h)
        self.grid_rowconfigure(2, weight=1, minsize=0)

        self.left_frame = tk.Frame(self, width=self.w - self.w_right_frame, height=self.h, relief=tk.GROOVE, bd=2)
        self.left_frame.grid(row=1, column=1, sticky="nsew")
        self.left_frame.grid_propagate(False)

        self.right_frame = tk.Frame(self, width=self.w_right_frame, height=self.h, relief=tk.GROOVE, bd=2)
        self.right_frame.grid(row=1, column=2, sticky="nsew")
        self.right_frame.grid_propagate(False)

        self.__setup_left_frame()
        self.__setup_right_frame()

    def __setup_left_frame(self):
        tk.Label(self.left_frame, text=self.title_name).grid(row=0, column=0, columnspan=2, sticky="nsew", pady=10)

        tk.Label(self.left_frame, text="Вопрос").grid(row=1, column=0, sticky="sew")
        self.text_widget = tk.Text(self.left_frame, height=5, width=75, highlightthickness=2,
                                   highlightcolor="grey", highlightbackground="lightgrey", font=("Arial", 10))
        self.text_widget.grid(row=2, column=0, columnspan=2, sticky="nsw", pady=5, padx=5)
        if self.question_text:
            self.text_widget.insert("1.0", self.question_text.get())

        separator = tk.Frame(self.left_frame, height=2, bd=1, relief=tk.SUNKEN, bg='gray')
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        options_lbl = tk.Label(self.left_frame, text="Варианты ответов")
        options_lbl.grid(row=4, column=0, sticky="sew")

        self.options_widgets = []
        for ind in range(3):
            option_lbl = tk.Label(self.left_frame, text=f"Вариант ответа {ind + 1}")
            option_lbl.grid(row=ind + 5, column=0, sticky="nsew", padx=5, pady=10)
            option_text_widget = tk.Text(self.left_frame, height=3, width=56, highlightthickness=2,
                                         highlightcolor="grey", highlightbackground="lightgrey", font=("Arial", 10))
            option_text_widget.grid(row=ind + 5, column=1, sticky="nsw", pady=5, padx=5)
            self.options_widgets.append(option_text_widget)
            if self.options:
                option_text_widget.insert("1.0", self.options[ind + 1])

        separator = tk.Frame(self.left_frame, height=2, bd=1, relief=tk.SUNKEN, bg='gray')
        separator.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        tk.Label(self.left_frame, text="Правильный ответ").grid(row=9, column=0, padx=10, pady=5, sticky="sn")
        correct_spinbox = tk.Spinbox(self.left_frame, from_=1, to=3, textvariable=self.correct_answer,
                                     state='readonly', width=10)
        correct_spinbox.grid(row=9, column=1, padx=5, pady=5, sticky="nsw")

        tk.Label(self.left_frame, text="Сложность").grid(row=10, column=0, padx=10, pady=5, sticky="ns")
        difficulty_spinbox = tk.Spinbox(self.left_frame, from_=1, to=9, textvariable=self.difficulty,
                                        state='readonly', width=10)
        difficulty_spinbox.grid(row=10, column=1, padx=5, pady=5, sticky="snw")

        tk.Label(self.left_frame, text="Метрика").grid(row=11, column=0, padx=10, pady=5, sticky="ns")
        type_combo = ttk.Combobox(self.left_frame, textvariable=self.question_type, values=["POL", "CHL", "UMN"],
                                  width=10, state='readonly')
        type_combo.grid(row=11, column=1, padx=5, pady=5, sticky="snw")

    def __setup_right_frame(self):
        action_btn = tk.Button(self.right_frame, text=self.action_button_text, command=self.__save_changes)
        action_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

        exit_btn = tk.Button(self.right_frame, text="Отмена", command=self.close_menu)
        exit_btn.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))

    def __save_changes(self):
        q_text = self.text_widget.get('1.0', tk.END).strip()
        if not q_text:
            messagebox.showwarning("Предупреждение", "Введите вопрос")
            return

        q_options = {}
        for i, entry in enumerate(self.options_widgets, 1):
            text = entry.get('1.0', tk.END).strip()
            if text:
                q_options[str(i)] = text
            else:
                messagebox.showwarning("Предупреждение", f"Введите вариант ответа {i}")
                return

        if self.question_id:
            self.repository.update_question(
                self.question_id,
                q_text,
                q_options,
                int(self.correct_answer.get()),
                int(self.difficulty.get()),
                self.question_type.get())
        else:
            self.repository.create_question(
                q_text,
                q_options,
                int(self.correct_answer.get()),
                int(self.difficulty.get()),
                self.question_type.get())

        self.__close_menu_with_update()
        messagebox.showinfo("Успех", self.exit_message)

    def __close_menu_with_update(self):
        self.close_menu()
        self.parent.reset_filters()
        self.parent.load_data()
