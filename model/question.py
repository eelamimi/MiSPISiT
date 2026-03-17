import json


class Question:
    def __init__(self, q: tuple):
        self.id: int = q[0]
        self.text: str = q[1]
        self.options: dict[int, str] = self.__get_options(q[2])
        self.answer: int = q[3]
        self.difficulty: int = q[4]
        self.type: int = q[5]
        self.__dumped_options = json.dumps(self.options, ensure_ascii=False)

    def __str__(self):
        return f"{self.id} {self.text} {self.options} {self.answer} {self.difficulty} {self.type}"

    @staticmethod
    def __keys_to_int(obj):
        if isinstance(obj, dict):
            return {int(k) if k.isdigit() else k: v for k, v in obj.items()}
        return obj

    def __get_options(self, options):
        return json.loads(options, object_hook=self.__keys_to_int)

    def is_correct_answer(self, option: int) -> bool:
        return self.answer == option

    def format_options(self):
        n = 20
        preview = ", ".join([f"{k}: {v[:n]}..." if len(v) > n else f"{k}: {v}" for k, v in self.options.items()])
        return preview

    def dump_options(self):
        return self.__dumped_options
