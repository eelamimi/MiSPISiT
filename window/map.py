import tkinter as tk
from collections import defaultdict

from model.result import Result
from window.base import ChildWindow


class MapWindow(ChildWindow):
    def __init__(self, parent, name, results: list[Result]):
        self.h = 600
        self.pady = 50
        super().__init__(parent, 10, self.h)
        self.title(f"Дерево результатов студента {name}")
        self.results = results
        self.w_sq = self.h_sq = 90

        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.__draw_map_and_center()

    def __draw_map_and_center(self):
        x, y = 20, self.h - self.pady - self.h_sq
        sepx = 20

        amount_of_sections = 0
        children_coords = defaultdict(list)
        grouped = defaultdict(list)
        parent_coords = []

        for result in self.results:
            if '.' in result.full_section:
                # отрисовка
                coords = self.__draw_rectangle(x, y, result)
                x += self.w_sq + sepx

                # группировка
                section = result.full_section[:-2]
                grouped[section].append(result)
                children_coords[section].append(coords)
        w = x
        parent_results = []
        for section, results in sorted(grouped.items(), key=lambda item: item[0]):
            pol = chl = umn = pol_c = chl_c = umn_c = 0
            for result in results:
                pol += result.pol
                chl += result.chl
                umn += result.umn
                pol_c += result.pol_c
                chl_c += result.chl_c
                umn_c += result.umn_c
            pol /= len(results)
            chl /= len(results)
            umn /= len(results)
            pol_c /= len(results)
            chl_c /= len(results)
            umn_c /= len(results)
            parent_results.append(Result((
                section,
                round(pol_c, 2), round(chl_c, 2), round(umn_c, 2),
                round(pol, 2), round(chl, 2), round(umn, 2))))
            amount_of_sections += 1

        x = (x - amount_of_sections * self.w_sq - (amount_of_sections - 1) * sepx) / 2
        y = self.h - self.pady - self.h_sq - (self.h - (self.pady + self.h_sq) * 2 - self.h_sq) / 2 - self.h_sq

        pol_f = chl_f = umn_f = pol_c_f = chl_c_f = umn_c_f = 0

        for result in parent_results:
            coords = self.__draw_rectangle(x, y, result)
            x += self.w_sq + sepx

            for child_coords in children_coords[result.full_section]:
                self.__draw_line(child_coords[0], coords[1])
            parent_coords.append(coords[0])

            # подсчёт за весь курс
            pol_f += result.pol
            chl_f += result.chl
            umn_f += result.umn
            pol_c_f += result.pol_c
            chl_c_f += result.chl_c
            umn_c_f += result.umn_c

        final_coords = self.__draw_rectangle(
            w // 2 - self.w_sq // 2, self.pady,
            Result(('Курс',
                    round(pol_c_f / amount_of_sections, 2),
                    round(chl_c_f / amount_of_sections, 2),
                    round(umn_c_f / amount_of_sections, 2),
                    round(pol_f / amount_of_sections, 2),
                    round(chl_f / amount_of_sections, 2),
                    round(umn_f / amount_of_sections, 2))))

        for coords in parent_coords:
            self.__draw_line(coords, final_coords[1])

        self.center_window(self, w, self.h)

    def __draw_rectangle(self, x_init: float, y_init: float, result: Result) -> tuple[
        tuple[float, float], tuple[float, float]]:
        y0_upper = y_init
        y1_lower = y0_upper + self.h_sq
        for i, mc in enumerate(((result.pol, result.pol_c), (result.chl, result.chl_c), (result.umn, result.umn_c))):
            m, c = mc

            x0_both = x_init + self.w_sq / 3 * i
            x1_both = x0_both + self.w_sq / 3
            y0_lower = y1_upper = y0_upper + self.h_sq * (1 - m)

            if m != 0:
                self.canvas.create_rectangle(x0_both, y0_lower, x1_both, y1_lower, outline='black', fill='gray')
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

    def __draw_line(self, coords0: tuple[float, float], coords1: tuple[float, float]) -> None:
        self.canvas.create_line(coords0, coords1, fill='black')