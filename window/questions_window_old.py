import json
import tkinter as tk
from tkinter import ttk, messagebox

from .base import ChildWindow


class QuestionsWindow(ChildWindow):
    def __init__(self, questions, parent, w, h):
        super().__init__(parent, w, h)
        self.questions = questions
        self.answers = {}

        self.title_label = ttk.Label(self, text="Ответьте на вопросы:")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky="w", padx=10)

        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=5)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(len(self.questions), weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Создаем фреймы для каждого вопроса
        self.question_frames = []

        for i, question_data in enumerate(self.questions):
            question_id, question_text, options_json, *rest = question_data

            frame = ttk.LabelFrame(self.main_frame, text=f"Вопрос {i + 1}", relief="solid", borderwidth=1)
            frame.grid(row=i, column=0, sticky="ew", pady=8, padx=5)
            frame.grid_columnconfigure(0, weight=1)
            self.question_frames.append(frame)

            question_label = ttk.Label(frame, text=question_text, wraplength=550)
            question_label.grid(row=0, column=0, sticky="w", pady=(8, 12), padx=10)

            options = json.loads(options_json)

            var = tk.StringVar(value="")
            self.answers[question_id] = var

            for j, (key, value) in enumerate(options.items()):
                rb = ttk.Radiobutton(frame, text=value, variable=var, value=key)
                rb.grid(row=j + 1, column=0, sticky="w", padx=20, pady=3)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, sticky="e", pady=15, padx=10)

        save_button = ttk.Button(button_frame, text="Сохранить ответы",
                                 command=self.save_answers)
        save_button.grid(row=0, column=1, padx=5)

        close_button = ttk.Button(button_frame, text="Закрыть", command=self.return_to_main)
        close_button.grid(row=0, column=0, padx=5)

    def save_answers(self):
        results = {
            'type': self.questions[0][6],
            'answers': list()
        }
        unanswered = []
        points = 0
        for i, question_data in enumerate(self.questions):
            question_id, _, options, correct_answer, *_ = question_data
            selected_answer = self.answers[question_id].get()

            if selected_answer:
                results['answers'].append({
                    'correct_answer': correct_answer,
                    'answer': selected_answer,
                    'question_number': i + 1
                })
                if int(selected_answer) == correct_answer:
                    points += (1 / 3) / len(self.questions)
            else:
                unanswered.append(i + 1)

        if unanswered:
            messagebox.showwarning(
                "Не все вопросы отвечены",
                f"Пожалуйста, ответьте на вопросы: {', '.join(map(str, unanswered))}"
            )
            return

        result_text = "\n".join([
            f"Вопрос {r['question_number']}: {r['answer']}"
            for r in results['answers']
        ])

        messagebox.showinfo("Ответы сохранены",
                            f"Все ответы успешно сохранены:\n{result_text}")

        self.parent.save_results(points, results['type'])
        self.return_to_main_to_main()
