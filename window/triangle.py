from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from window.base import ChildWindow


class TriangleWindow(ChildWindow):
    def __init__(self, parent, module, name, pol_c_f, chl_c_f, umn_c_f, pol_f, chl_f, umn_f):
        super().__init__(parent, 600, 500)
        self.title = f"Успешность студента {name}"
        self.__draw_triangles(pol_c_f, chl_c_f, umn_c_f,
                              round(pol_c_f * pol_f, 2),
                              round(chl_c_f * chl_f, 2),
                              round(umn_c_f * umn_f, 2))

    def __draw_triangles(self, m_p_c, m_c_c, m_u_c, p_c, c_c, u_c):
        fig = Figure(figsize=(6, 5), dpi=100)
        self.ax = fig.add_subplot(111, projection='3d')

        self.__draw_triangle(m_c_c, m_u_c, m_p_c)
        self.__draw_triangle(c_c, u_c, p_c, ls='--')
        self.__draw_point(0, 0, 0)

        self.__axis_settings(m_p_c, m_c_c, m_u_c, p_c, c_c, u_c)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def __draw_triangle(self, x, y, z, ls='-', lw=3, labels: list[str] | None = None):
        if labels is None:
            self.ax.plot([x, 0.0], [0.0, y], [0.0, 0.0], color='r', linestyle=ls, linewidth=lw)
            self.ax.plot([0.0, 0.0], [y, 0.0], [0.0, z], color='g', linestyle=ls, linewidth=lw)
            self.ax.plot([0.0, x], [0.0, 0.0], [z, 0.0], color='b', linestyle=ls, linewidth=lw)
        else:
            self.ax.plot([x, 0.0], [0.0, y], [0.0, 0.0], color='r', linestyle=ls, linewidth=lw, label=labels[0])
            self.ax.plot([0.0, 0.0], [y, 0.0], [0.0, z], color='g', linestyle=ls, linewidth=lw, label=labels[1])
            self.ax.plot([0.0, x], [0.0, 0.0], [z, 0.0], color='b', linestyle=ls, linewidth=lw, label=labels[2])

    def __draw_point(self, x, y, z, c='black', r=25):
        self.ax.scatter([x], [y], [z], color=c, s=r)

    def __axis_settings(self, m_p_c, m_c_c, m_u_c, p_c, c_c, u_c):
        self.ax.set_xlim(0, m_c_c + .5)
        self.ax.set_ylim(0, m_u_c + .5)
        self.ax.set_zlim(0, m_p_c + .5)

        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        self.ax.disable_mouse_rotation()
        self.ax.view_init(30, 45)

        self.ax.set_xlabel('SC')
        self.ax.set_ylabel('SU')
        self.ax.set_zlabel('SP')

        success = self.__calculate_volume(p_c, c_c, u_c) / self.__calculate_volume( m_p_c, m_c_c, m_u_c)
        self.ax.set_title(f'У(УК) = {round(success, 2)}')

    def __calculate_volume(self, p_c, c_c, u_c) -> int:
        s = c_c * u_c / 2
        v = s * p_c / 3
        return round(v, 2)
