import json


class Question:
    def __init__(self, q: tuple):
        self.id = q[0]
        self.text = q[1]
        self.options = self.__get_options(q[2])
        self.answer = q[3]
        self.difficulty = q[4]
        self.group = q[5]
        self.type = q[6]

    def __str__(self):
        return f"{self.id} {self.text} {self.options} {self.answer} {self.difficulty} {self.group} {self.type}"

    @staticmethod
    def __keys_to_int(obj):
        if isinstance(obj, dict):
            return {int(k) if k.isdigit() else k: v for k, v in obj.items()}
        return obj

    def __get_options(self, options):
        return json.loads(options, object_hook=self.__keys_to_int)
