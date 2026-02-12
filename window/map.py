from window.base import ChildWindow


class MapWindow(ChildWindow):
    def __init__(self, parent, results):
        super().__init__(parent, 600, 900)
        self.title("Дерево результатов")
        self.results = results