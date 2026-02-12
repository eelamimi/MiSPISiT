import sqlite3

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from .base import DiagnosticModule


class DiagnosticModuleTree(DiagnosticModule):
    def __init__(self, db_name='education.db', init_database=False):
        super().__init__(db_name, init_database)

    def create_results_tree(self, student_id=1):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('''
                SELECT section, pol, chl, umn 
                FROM Results 
                WHERE student_id = ? 
                ORDER BY id
            ''', (student_id,))

        data = cursor.fetchall()

        hierarchy = {
            'Итоговый': {'pol': 0, 'chl': 0, 'umn': 0, 'children': {}},
            'children_count': len(data)
        }

        for section, pol, chl, umn in data:
            pol = 0 if pol is None else pol
            chl = 0 if chl is None else chl
            umn = 0 if umn is None else umn
            if section == 'Итоговый':
                hierarchy['Итоговый']['pol'] = pol
                hierarchy['Итоговый']['chl'] = chl
                hierarchy['Итоговый']['umn'] = umn
            else:
                main_section = section.split('.')[0]  # 'РД 1'
                sub_section = section  # 'РД 1.1.'

                if main_section not in hierarchy['Итоговый']['children']:
                    hierarchy['Итоговый']['children'][main_section] = {
                        'pol': [], 'chl': [], 'umn': [], 'children': {}
                    }
                hierarchy_sub_section = hierarchy['Итоговый']['children'][main_section]['children'].get(
                    sub_section, {})
                hierarchy_sub_section = {
                    'pol': pol + hierarchy_sub_section.get('pol', 0),
                    'chl': chl + hierarchy_sub_section.get('chl', 0),
                    'umn': umn + hierarchy_sub_section.get('umn', 0)
                }
                hierarchy['Итоговый']['children'][main_section]['children'][sub_section] = hierarchy_sub_section
                hierarchy['Итоговый']['children'][main_section]['pol'].append(pol)
                hierarchy['Итоговый']['children'][main_section]['chl'].append(chl)
                hierarchy['Итоговый']['children'][main_section]['umn'].append(umn)

        for main_section in hierarchy['Итоговый']['children']:
            section_data = hierarchy['Итоговый']['children'][main_section]
            section_data['pol'] = np.mean(section_data['pol'])
            section_data['chl'] = np.mean(section_data['chl'])
            section_data['umn'] = np.mean(section_data['umn'])

        conn.close()
        return hierarchy

    def plot_results_tree(self, hierarchy=None, student_id=1):
        def line(x1, y1, x2, y2, color='black'):
            plt.plot([x1, x2], [y1, y2], color=color)

        def box_with_text(x, y, w, h, text):
            ax.add_patch(
                patches.Rectangle(
                    (x, y), w, h,
                    facecolor='lightgray',
                    edgecolor='black',
                    linewidth=2
                )
            )
            ax.text(
                x + w / 2, y + h / 2, text,
                ha='center', va='center',
                fontsize=7, fontweight='bold'
            )

        max_x, max_y = 20, 8
        hierarchy = self.create_results_tree(student_id) if hierarchy is None else hierarchy
        len_children = hierarchy['children_count']
        ind_subsection = 0
        fig, ax = plt.subplots()
        final = hierarchy['Итоговый']
        pol, chl, umn = final["pol"], final["chl"], final["umn"]
        chn = (pol + chl + umn) / 3
        main_sections = list(hierarchy['Итоговый']['children'].keys())
        x_final, y_final, w_box, h_box = 9.25, max_y - 1.5, 1.5, 1.2,
        box_with_text(x_final, y_final, w_box, h_box,
                      f'Итоговый\n\nPOL = {pol:.1f}\nCHL = {chl:.1f}\nUMN = {chl:.1f}\nCHN = {chn:.1f}')

        for i, main_section in enumerate(main_sections):
            x_main, y_main = 1 + (max_x / len(main_sections)) * i, max_y - .5 - max_y / 2
            main = hierarchy['Итоговый']['children'][main_section]
            pol, chl, umn = main["pol"], main["chl"], main["umn"]
            chn = (pol + chl + umn) / 3
            box_with_text(x_main, y_main, w_box, h_box,
                          f'{main_section}\n\nPOL = {pol:.2f}\nCHL = {chl:.2f}\nUMN = {chl:.2f}\nCHN = {chn:.2f}')
            line(x_main + w_box / 2, y_main + h_box, x_final + w_box / 2, y_final)

            subsections = list(main['children'].keys())
            for subsection in subsections:
                x_sub, y_sub = .5 + (max_x / len_children) * ind_subsection, .5
                sub = main['children'][subsection]
                pol, chl, umn = sub["pol"], sub["chl"], sub["umn"]
                chn = (pol + chl + umn) / 3
                box_with_text(x_sub, y_sub, w_box - .4, h_box,
                              f'{subsection}\n\nPOL = {pol:.2f}\nCHL = {chl:.2f}\nUMN = {chl:.2f}\nCHN = {chn:.2f}')
                line(x_sub + (w_box - .4) / 2, y_sub + h_box, x_main + w_box / 2, y_main)
                ind_subsection += 1

        ax.set_xlim(0, max_x)
        ax.set_ylim(0, max_y)
        ax.set_aspect('equal')
        plt.title(f'Дерево результатов студента {student_id}',
                  fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    dm = DiagnosticModuleTree(init_database=True)
    # print(dm.create_results_tree(2))
    # dm.display_student_results()
    # dm.plot_results_tree()
