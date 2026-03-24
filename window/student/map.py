import tkinter as tk
from collections import defaultdict

from model.result import Result
from window.child import ChildWindow
from window.student.triangle import TriangleWindow


class MapWindow(ChildWindow):
    def __init__(self, parent, module, name, results: list[Result]):
        self.h = 600
        self.pady = 50
        self.name = name
        self.module = module
        super().__init__(parent, 10, self.h)
        self.title(f"Дерево результатов студента {self.name}")
        self.results = results
        self.w_sq = self.h_sq = 90

        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.__draw_map_and_center()

    def __draw_map_and_center(self):
        x, y = 20, self.h - self.pady - self.h_sq
        separator_x = 20

        amount_of_sections = 0
        children_coordinates = defaultdict(list)
        grouped = defaultdict(list)
        parent_coordinates = []

        for result in self.results:
            if '.' in result.full_section:
                # отрисовка
                coordinates = self.__draw_rectangle(x, y, result)
                x += self.w_sq + separator_x

                # группировка
                section = result.full_section[:-2]
                grouped[section].append(result)
                children_coordinates[section].append(coordinates)
        w = x
        parent_results = []
        for section, results in sorted(grouped.items(), key=lambda item: item[0]):
            pol = chl = umn = pol_c = chl_c = umn_c = 0
            for result in results:
                pol += result.pol
                chl += result.chl
                umn += result.umn
                pol_c = max(result.pol_c, pol_c)
                chl_c = max(result.chl_c, chl_c)
                umn_c = max(result.umn_c, umn_c)
            pol /= len(results)
            chl /= len(results)
            umn /= len(results)
            parent_results.append(Result((
                section,
                round(pol_c, 2), round(chl_c, 2), round(umn_c, 2),
                round(pol, 2), round(chl, 2), round(umn, 2))))
            amount_of_sections += 1

        x = (x - amount_of_sections * self.w_sq - (amount_of_sections - 1) * separator_x) / 2
        y = self.h - self.pady - self.h_sq - (self.h - (self.pady + self.h_sq) * 2 - self.h_sq) / 2 - self.h_sq

        self.pol_f = self.chl_f = self.umn_f = self.pol_c_f = self.chl_c_f = self.umn_c_f = 0

        for result in parent_results:
            coordinates = self.__draw_rectangle(x, y, result)
            x += self.w_sq + separator_x

            for child_coordinates in children_coordinates[result.full_section]:
                self.__draw_line(child_coordinates[0], coordinates[1])
            parent_coordinates.append(coordinates[0])

            # подсчёт за весь курс
            self.pol_f += result.pol
            self.chl_f += result.chl
            self.umn_f += result.umn
            self.pol_c_f = max(result.pol_c, self.pol_c_f)
            self.chl_c_f = max(result.chl_c, self.chl_c_f)
            self.umn_c_f = max(result.umn_c, self.umn_c_f)

        self.pol_f = round(self.pol_f / amount_of_sections, 2)
        self.chl_f = round(self.chl_f / amount_of_sections, 2)
        self.umn_f = round(self.umn_f / amount_of_sections, 2)

        final_coordinates = self.__draw_rectangle(
            w // 2 - self.w_sq // 2, self.pady,
            Result(('Учебный курс',
                    self.pol_c_f, self.chl_c_f, self.umn_c_f,
                    self.pol_f, self.chl_f, self.umn_f)))

        for coordinates in parent_coordinates:
            self.__draw_line(coordinates, final_coordinates[1])

        self.center_window(self, w, self.h)

    def __draw_rectangle(self, x_init: float, y_init: float, result: Result) ->\
            tuple[tuple[float, float], tuple[float, float]]:
        y0_upper = y_init
        y1_lower = y0_upper + self.h_sq
        for i, mc in enumerate(((result.pol, result.pol_c), (result.chl, result.chl_c), (result.umn, result.umn_c))):
            m, c = mc

            x0_both = x_init + self.w_sq / 3 * i
            x1_both = x0_both + self.w_sq / 3
            y0_lower = y1_upper = y0_upper + self.h_sq * (1 - m)

            if m != 0:
                self.canvas.create_rectangle(x0_both, y0_lower, x1_both, y1_lower, outline='black', fill='gray')
            if m != 1:
                self.canvas.create_rectangle(x0_both, y0_upper, x1_both, y1_upper, outline='black', fill='white')

            x_t = (x0_both + x1_both) / 2
            m_t = "POL" if i == 0 else "CHL" if i == 1 else "UMN"
            self.canvas.create_text(x_t, y1_lower + 10, text=m_t)
            self.canvas.create_text(x_t, y1_lower - 10, text=str(c))
            self.canvas.create_text(x_t, y0_upper + 10, text=str(m))

        x0_t_section = x_init + self.w_sq / 3 * 1
        x1_t_section = x0_t_section + self.w_sq / 3
        x_t_section = (x0_t_section + x1_t_section) / 2
        y_t_section = y0_upper - 10
        self.canvas.create_text(x_t_section, y_t_section, text=result.full_section)

        return (x_t_section, y_t_section - 10), (x_t_section, y1_lower + 20)

    def __draw_line(self, coordinates0: tuple[float, float], coordinates1: tuple[float, float]) -> None:
        self.canvas.create_line(coordinates0, coordinates1, fill='black')

    def exit_action(self):
        self.destroy()
        triangle_window = TriangleWindow(self.parent, self.name,
                                         self.pol_c_f, self.chl_c_f, self.umn_c_f,
                                         self.pol_f, self.chl_f, self.umn_f)
        triangle_window.show()
