import json
import tkinter as tk
from tkinter import ttk, messagebox

from db.repository import Repository
from window.main import MainWindow
from window.teacher.question_detail import QuestionDetailWindow
from window.teacher.view_options import ViewOptionsWindow


class QuestionApp(MainWindow):
    def __init__(self, repository: Repository):
        super().__init__(1200, 600)
        self.title("Управление вопросами")
        self.repository = repository

        self.text_var = tk.StringVar()
        self.difficulty_var = tk.StringVar(value="Все")
        self.metric_var = tk.StringVar(value="Все")

        self.create_widgets()
        self.create_context_menu()
        self.load_data()

    def create_widgets(self):
        filter_frame = ttk.LabelFrame(self, text="Фильтры", padding=10)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Поиск:").grid(row=0, column=0, padx=5)
        tk.Entry(filter_frame, textvariable=self.text_var, width=40).grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Сложность:").grid(row=0, column=2, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.difficulty_var, values=["Все"] + list(range(1, 10)), width=10,
                     state='readonly').grid(row=0, column=3, padx=5)

        tk.Label(filter_frame, text="Метрика:").grid(row=0, column=4, padx=5)
        ttk.Combobox(filter_frame, textvariable=self.metric_var, values=["Все", "POL", "CHL", "UMN"], width=10,
                     state='readonly').grid(row=0, column=5, padx=5)

        tk.Button(filter_frame, text="Применить", command=self.apply_filters).grid(row=0, column=6, padx=5)
        tk.Button(filter_frame, text="Сбросить", command=self.reset_filters).grid(row=0, column=7, padx=5)

        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scroll_y = tk.Scrollbar(table_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            table_frame,
            columns=("id", "text", "options", "correct_answer", "difficulty", "type"),
            show="headings",
            yscrollcommand=scroll_y.set
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("text", text="Вопрос")
        self.tree.heading("options", text="Варианты ответов")
        self.tree.heading("correct_answer", text="Правильный ответ")
        self.tree.heading("difficulty", text="Сложность")
        self.tree.heading("type", text="Тип")

        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("text", width=300)
        self.tree.column("options", width=400)
        self.tree.column("correct_answer", width=100, anchor=tk.CENTER)
        self.tree.column("difficulty", width=80, anchor=tk.CENTER)
        self.tree.column("type", width=80, anchor=tk.CENTER)

        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll_y.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", lambda e: self.edit_question())

        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Button(button_frame, text="Добавить", command=self.add_question).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Редактировать", command=self.edit_question).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Удалить", command=self.delete_question).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Обновить", command=self.load_data).pack(side=tk.LEFT, padx=5)

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Редактировать", command=self.edit_question)
        self.context_menu.add_command(label="Удалить", command=self.delete_question)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Просмотреть варианты", command=self.view_options)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def load_data(self):
        for q in self.tree.get_children():
            self.tree.delete(q)

        questions = self.repository.get_questions_with_filters(
            self.text_var.get().strip(),
            self.difficulty_var.get(),
            self.metric_var.get())

        for q in questions:
            self.tree.insert("", tk.END,
                             values=(q.id, q.text, q.format_options(), q.answer, q.difficulty, q.type),
                             tags=(q.dump_options(),))

    def apply_filters(self):
        self.load_data()

    def reset_filters(self):
        self.text_var.set("")
        self.difficulty_var.set("Все")
        self.metric_var.set("Все")
        self.load_data()

    def add_question(self):
        self.open_question_window()

    def edit_question(self):
        question_id = self._get_question_id("Выберите вопрос для редактирования")
        self.open_question_window(question_id)

    def delete_question(self):
        question_id = self._get_question_id("Выберите вопрос для удаления")

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот вопрос?"):
            self.repository.delete_question_by_id(question_id)

            self.reset_filters()
            self.load_data()
            messagebox.showinfo("Успех", "Вопрос удален")

    def _get_question_id(self, message):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", message)
            return
        item = self.tree.item(selected[0])
        return item['values'][0]

    def view_options(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        options = json.loads(item['tags'][0])

        view_options_window = ViewOptionsWindow(self, item['values'][1], options, item['values'][3])
        view_options_window.show()

    def open_question_window(self, question_id=None):
        question_detail_window = QuestionDetailWindow(self, self.repository, question_id)
        question_detail_window.show()


def main_teacher():
    app = QuestionApp(Repository(init_database=True))
    app.mainloop()


if __name__ == "__main__":
    main_teacher()
