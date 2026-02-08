import asyncio
import threading
import tkinter as tk
from tkinter import font
from tkinter import messagebox

from base import ChildWindow


class TestModule(ChildWindow):
    def __init__(self, parent, questions, results, part):
        super().__init__(parent, 300, 450)
        self.questions = questions
        self.results = results
        self.part = part
        self.index = 0
        self.yes_no = tk.BooleanVar(value=True)
        self.count_yes = 0
        self.len = len(self.questions)
        self.timer_active = False
        self.current_loop = None

        # Создаем шрифт размером 14 пикселей
        self.custom_font = font.Font(family="Helvetica", size=14)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.timer = tk.Label(self, text="30", font=self.custom_font)
        self.timer.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky='nsew')

        self.lecture_lbl = tk.Label(
            self,
            text=f"№ {self.index + 1}\tЛекция: {self.questions[self.index].lecture}\tТип: {self.questions[self.index].type}",
            justify="left",
            wraplength=300,
            font=self.custom_font
        )
        self.lecture_lbl.grid(row=2, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.question_lbl = tk.Label(
            self,
            text=self.questions[self.index].text,
            justify="left",
            wraplength=300,
            font=self.custom_font
        )
        self.question_lbl.grid(row=3, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.update_idletasks()
        new_w = self.question_lbl.winfo_reqwidth() + 50
        self.center_window(self, new_w if new_w > 300 else 300, 450)

        self.yes_rb = tk.Radiobutton(
            self,
            text='Правильно',
            variable=self.yes_no,
            value=True,
            font=self.custom_font
        )
        self.yes_rb.grid(row=4, column=1, pady=10)

        self.no_rb = tk.Radiobutton(
            self,
            text='Неправильно',
            variable=self.yes_no,
            value=False,
            font=self.custom_font
        )
        self.no_rb.grid(row=5, column=1, pady=10)

        self.next_btn = tk.Button(
            self,
            text="Следующий вопрос",
            command=self.next_question,
            font=self.custom_font
        )
        self.next_btn.grid(row=6, column=2, pady=10)
        self.start_timer()

    async def countdown_timer(self):
        for i in range(30):
            await asyncio.sleep(1)
            if not self.timer_active or self.timer['text'] == '0':
                break
            self.after(0, lambda l=self.timer: l.config(text=str(int(self.timer['text']) - 1)))

        if self.timer_active:
            self.yes_no.set(False)
            self.after(0, lambda: self.next_question())

    def start_timer(self):
        self.timer_active = True
        loop = asyncio.new_event_loop()
        self.current_loop = loop
        asyncio.set_event_loop(loop)
        thread = threading.Thread(target=loop.run_forever)
        thread.daemon = True
        thread.start()
        asyncio.run_coroutine_threadsafe(self.countdown_timer(), loop)

    def stop_timer(self):
        self.timer_active = False
        if self.current_loop:
            self.current_loop.call_soon_threadsafe(self.current_loop.stop)
            self.current_loop = None

    def next_question(self):
        self.stop_timer()

        self.index += 1
        if self.yes_no.get():
            self.count_yes += 1
        if self.index >= self.len:
            messagebox.showinfo(
                title="Результат",
                message=f"Правильных ответов: {self.count_yes}\n"
                        f"Неправильных ответов: {self.len - self.count_yes}\n\n"
                        f"Баллов: {round(self.count_yes / 3 * 10)}"
            )
            self.results[self.questions[0].type + f" {self.part} тест"] = round(self.count_yes / 3 * 10)
            self.return_to_main()
            return
        elif self.index == self.len - 1:
            self.next_btn.config(text="Закончить тестирование")
        self.timer.config(text='30')
        self.question_lbl.config(text=self.questions[self.index].text)
        self.lecture_lbl.config(
            text=f"№ {self.index + 1}\tЛекция: {self.questions[self.index].lecture}\tТип: {self.questions[self.index].type}")
        self.update_idletasks()
        new_w = self.question_lbl.winfo_reqwidth() + 50
        self.center_window(self, new_w if new_w > 300 else 300, 450)
        self.start_timer()
