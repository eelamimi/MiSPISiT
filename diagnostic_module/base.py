import json
import sqlite3
from collections import defaultdict
from datetime import datetime

from model.question import Question
from model.result import Result

class DiagnosticModule:
    def __init__(self, db_name='education.db', init_database=False):
        self.db_name = db_name
        if init_database:
            self.__init_database()
            print("database initialized")

    def __init_database(self):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        try:
            cursor = conn.cursor()

            try:
                cursor.execute('DELETE FROM `Students`;')
                cursor.execute('DELETE FROM `Questions`;')
                cursor.execute('DELETE FROM `Results`;')

                cursor.execute('DROP TABLE `Students`')
                cursor.execute('DROP TABLE `Questions`;')
                cursor.execute('DROP TABLE `Results`;')
            except Exception as e:
                print(e)

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS `Students` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` TEXT NOT NULL);''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS `Questions` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `text` TEXT NOT NULL,
                `options` JSON NOT NULL,
                `correct_answer` INTEGER NOT NULL,
                `difficulty` INTEGER DEFAULT 1,
                `type` TEXT NOT NULL CHECK(`type` IN (\'POL\', \'CHL\', \'UMN\')));''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS `Results` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `student_id` INTEGER,
                `section` TEXT,
                `test_date` TEXT,
                `pol_c` INTEGER NOT NULL,
                `chl_c` INTEGER NOT NULL,
                `umn_c` INTEGER NOT NULL,
                `pol` REAL,
                `chl` REAL,
                `umn` REAL,
                FOREIGN KEY (`student_id`) REFERENCES Students (`id`));''')

            DiagnosticModule.__init_student(cursor)

            pol_first = (
                ("Что представляет собой предметная область?", json.dumps(
                    {1: "Это программный код, реализующий функции системы.",
                     2: "Это часть реального мира, которую исследует или автоматизирует система.",
                     3: "Это графическая схема базы данных."}), 2),
                ("Какие элементы включает контекстная диаграмма?", json.dumps(
                    {1: "Все функциональные блоки системы и их интерфейсы.",
                     2: "Единственный функциональный блок, представляющий систему в целом, и ее внешние сущности.",
                     3: "Структуру данных и алгоритмы работы системы."}), 2),
                ("Чем занимается методология SADT?", json.dumps(
                    {1: "Структурным анализом и проектированием сложных систем.",
                     2: "Только разработкой диаграмм потоков данных (DFD).",
                     3: "Статистическим анализом данных предприятия."}), 1),
                ("Какова логика функционирования динамических систем согласно SADT?", json.dumps(
                    {1: "«Входные данные определяют управляющие воздействия».",
                     2: "«Управление определяет, как входные данные преобразуются в выходные, используя механизмы».",
                     3: "«Механизмы напрямую генерируют выходные данные из входных»."}), 2),
                ("Какие компоненты необходимы для создания контекстной диаграммы?", json.dumps(
                    {1: "Множество функциональных блоков и хранилища данных.",
                     2: "Один блок (система), внешние сущности, входы, выходы, управления и механизмы.",
                     3: "Объекты, их состояния и события, вызывающие переходы."}), 2)
            )
            pol_second = (
                ("Что такое проект?", json.dumps(
                    {1: "Процесс постоянного улучшения бизнес-процессов",
                     2: "Временное предприятие, направленное на создание уникального продукта, услуги или результата",
                     3: "Ежедневная операционная деятельность организации"}), 2),
                ("Назовите основные характеристики проекта.", json.dumps(
                    {1: "Повторяемость, стабильность, постоянство",
                     2: "Временность, уникальность, последовательное уточнение",
                     3: "Автоматизация, стандартизация, массовость"}), 2),
                ("Что такое жизненный цикл проекта?", json.dumps(
                    {1: "Список сотрудников, участвующих в проекте", 2: "Бюджетное планирование проекта по месяцам",
                     3: "Последовательность фаз от инициации до завершения проекта"}), 3),
                ("Какие существуют типы проектов?", json.dumps(
                    {1: "Только строительные и IT-проекты",
                     2: "Инвестиционные, организационные, социальные, инновационные и другие",
                     3: "Большие, средние и маленькие по размеру команды"}), 2),
                ("Что такое классическая модель проектирования?", json.dumps(
                    {1: "Итеративная модель с циклической разработкой",
                     2: "Гибкая методология Scrum с короткими спринтами",
                     3: "Последовательная модель (водопад) с четкими этапами"}), 3)
            )
            pol_third = (
                ("Что такое методы проектирования?", json.dumps(
                    {1: "Программные инструменты для рисования диаграмм",
                     2: "Совокупность приемов и операций для создания проекта системы",
                     3: "Документация по техническому заданию"}), 2),
                ("Что представляют собой средства проектирования?", json.dumps(
                    {1: "Теоретические концепции и подходы",
                     2: "Программные и аппаратные инструменты, поддерживающие процесс проектирования",
                     3: "Финансовые ресурсы проекта"}), 2),
                ("Что такое технологии проектирования?", json.dumps(
                    {1: "Отдельные приемы создания чертежей",
                     2: "Упорядоченная совокупность методов и средств проектирования",
                     3: "Процесс обучения проектировщиков"}), 2),
                ("Приведите пример методологии проектирования.", json.dumps(
                    {1: "Microsoft Visio",
                     2: "Scrum",
                     3: "SADT/IDEF0"}), 3),
                ("Опишите суть метода параметрического проектирования.", json.dumps(
                    {1: "Создание системы путем подбора готовых компонентов из библиотек",
                     2: "Проектирование на основе установления зависимостей между параметрами системы и автоматической генерации решений при их изменении",
                     3: "Последовательная ручная отрисовка каждого элемента системы без использования связей"}),
                 2)
            )

            chl_first = (
                ("Почему важно определять границы системы при создании контекстной диаграммы?", json.dumps(
                    {1: "Чтобы увеличить количество внешних связей системы",
                     2: "Чтобы четко отделить систему от внешней среды и определить область анализа",
                     3: "Это формальное требование стандартов документооборота"}), 2),
                ("Как используется методология SADT в современном проектировании?", json.dumps(
                    {1: "Исключительно как исторический пример ранних методов",
                     2: "В основном для графического оформления презентаций",
                     3: "Как основа для структурного анализа бизнес-процессов и требований, предшествующая детальному проектированию"}),
                 3),
                ("Каким образом определяются потоки данных в контекстной диаграмме?", json.dumps(
                    {1: "Путем прямого копирования потоков из технического задания без изменений",
                     2: "Через анализ взаимодействий между системой и внешними сущностями (что получает/отдает система)",
                     3: "На основе внутренних алгоритмов работы программных модулей"}), 2),
                ("Почему создаются классификационные схемы при проектировании информационных систем?", json.dumps(
                    {1: "Для усложнения документации и увеличения объема работ",
                     2: "Чтобы систематизировать информацию, выявить структуру предметной области и обеспечить однозначность терминов",
                     3: "Это требование исключительно для научных публикаций"}), 2),
                ("Каким образом формируются границы системы в процессе разработки моделей?", json.dumps(
                    {1: "Произвольно, на усмотрение проектировщика",
                     2: "Путем фиксации всех возможных внутренних компонентов без учета внешнего контекста",
                     3: "На основе целей моделирования, фокуса анализа и взаимодействий с внешними сущностями"}), 3)
            )
            chl_second = (
                ("Почему важен жизненный цикл проекта?", json.dumps(
                    {1: "Он гарантирует 100%-й успех проекта без рисков",
                     2: "Обеспечивает структурированный подход, определяет последовательность работ, контрольные точки и критерии перехода между этапами",
                     3: "Требуется только для формального отчета перед заказчиком"}), 2),
                ("Какова роль методологической модели в проекте?", json.dumps(
                    {1: "Она является юридическим договором между заказчиком и исполнителем",
                     2: "Определяет стандарты, процессы, роли и артефакты, обеспечивая управляемый и предсказуемый ход работ",
                     3: "Это просто рекомендованный список программного обеспечения для команды"}), 2),
                ("Как функционирует каскадная модель?", json.dumps(
                    {1: "В коротких итерациях (спринтах) с постоянным пересмотром требований",
                     2: "Последовательно, когда следующий этап начинается только после полного завершения предыдущего",
                     3: "Путем одновременной разработки всех компонентов системы"}), 2),
                ("В чём особенность спиральной модели?", json.dumps(
                    {1: "Полное отсутствие этапа тестирования до окончания проекта",
                     2: "Циклическая разработка с акцентом на оценку и минимизацию рисков на каждой итерации",
                     3: "Жесткая фиксация требований в самом начале проекта"}), 2),
                ("Зачем применяются инкрементные модели?", json.dumps(
                    {1: "Чтобы заморозить все требования и никогда их не менять",
                     2: "Для последовательной поставке заказчику готовых частей (инкрементов) продукта, что позволяет раньше получить ценность и получить обратную связь",
                     3: "Чтобы максимально усложнить процесс коммуникации в команде"}), 2)
            )
            chl_third = (
                ("Почему важна методологическая модель в проекте?", json.dumps(
                    {1: "Она является юридическим договором и имеет силу в суде",
                     2: "Обеспечивает стандартизацию процессов, предсказуемость результатов и эффективное управление ресурсами и рисками",
                     3: "Позволяет полностью избежать документирования на протяжении всего проекта"}), 2),
                ("Какими основными функциями обладают Agile-инструменты?", json.dumps(
                    {1: "Автоматическое написание кода без участия программистов",
                     2: "Визуализация рабочих процессов (канбан), отслеживание задач (task tracking), планирование итераций и облегчение коммуникации",
                     3: "Составление жестких графиков работ на несколько лет вперед без возможности изменений"}), 2),
                ("В чём особенность параметрического проектирования?", json.dumps(
                    {1: "Полное отсутствие каких-либо расчетов и формул",
                     2: "Создание модели, где элементы связаны параметрическими зависимостями, и изменение одного параметра автоматически обновляет всю связанную модель",
                     3: "Исключительно ручная отрисовка каждого варианта проекта"}), 2),
                ("Как внедряется методика Scrum?", json.dumps(
                    {1: "Путем единоразового обучения руководителя",
                     2: "Через формирование кросс-функциональных команд, введение ролей (Владелец продукта, Scrum-мастер), итеративную работу в спринтах с регулярными событиями (митинг, ретроспектива)",
                     3: "Установкой специального программного обеспечения на все компьютеры"}), 2),
                ("Каковы преимущества параметрического проектирования?", json.dumps(
                    {1: "Медленная скорость работы и увеличение количества ошибок",
                     2: "Быстрая генерация и анализ множества вариантов, поддержка сложных зависимостей, легкое внесение глобальных изменений в модель",
                     3: "Полная независимость от вычислительных мощностей компьютера"}), 2)
            )

            umn_first = (
                ("Какой элемент диаграммы потоков данных (DFD) показывает движение информации внутри системы?",
                 json.dumps(
                     {1: "Внешняя сущность", 2: "Поток данных", 3: "Хранилище данных"}), 2),
                ("Какая стратегия подойдет для уменьшения неопределенности при разработке новых продуктов?",
                 json.dumps({1: "Проведение тестирования пользователями",
                             2: "Игнорирование обратной связи клиентов",
                             3: "Фокус на долгосрочные прогнозы рынка"}), 1),
                ("В каком случае рекомендуется проводить первую итерацию функциональной декомпозиции?",
                 json.dumps(
                     {1: "После утверждения общего плана проекта", 2: "До начала любого проектирования",
                      3: "Сразу после окончания разработки первой версии продукта"}), 1),
                ("Что является основным преимуществом применения стандартизированных нотаций в проектировании?",
                 json.dumps({1: "Универсальность понимания среди членов команды",
                             2: "Высокая сложность схем и диаграмм",
                             3: "Возможность сократить количество используемых символов"}), 1),
                ("Что важнее всего учесть при создании классификационной схемы?", json.dumps(
                    {1: "Масштабируемость и устойчивость схемы", 2: "Применение ярких цветов и шрифтов",
                     3: "Использование максимального количества деталей"}), 1)
            )
            umn_second = (
                ("Какую стратегию используют для сокращения длительности проекта без ущерба качеству?",
                 json.dumps(
                     {1: "Минимизация количества контрольных точек", 2: "Сокращение объемов тестирования",
                      3: "Параллельное выполнение некоторых этапов"}), 3),
                ("Что произойдет, если игнорировать риски в управлении проектом?", json.dumps(
                    {1: "Возможны задержки и перерасход бюджета",
                     2: "Значительно улучшатся коммуникации в команде",
                     3: "Проект завершится раньше запланированного срока"}), 1),
                ("Какой критерий успешности проекта считается универсальным?", json.dumps(
                    {1: "Уровень удовлетворённости клиента", 2: "Количество проведенных совещаний",
                     3: "Доля участия руководителя проекта"}), 1),
                ("Каким образом минимизируются конфликты между заказчиком и исполнителем?", json.dumps(
                    {1: "Открытое обсуждение ожиданий и целей", 2: "Частые замены руководителей проекта",
                     3: "Уклонение от обсуждения разногласий"}), 1),
                ("Как снизить риск превышения бюджета в ходе проекта?", json.dumps(
                    {1: "Превентивное внесение изменений в дизайн",
                     2: "Планирование резерва на непредвиденные расходы",
                     3: "Отказ от согласования промежуточных результатов"}), 2)
            )
            umn_third = (
                ("Что увеличивает гибкость и производительность в параметрическом проектировании?", json.dumps(
                    {1: "Создание уникальных шаблонов для каждой детали",
                     2: "Повторное использование стандартных параметров",
                     3: "Исключение проверок перед внесением изменений"}), 2),
                ("В чем состоит основное отличие методики Scrum от классической водопадной модели?", json.dumps(
                    {1: "Scrum требует полного завершения каждого этапа",
                     2: "Scrum допускает одновременное выполнение нескольких фаз",
                     3: "Scrum исключает участие команды разработчиков"}), 2),
                ("Почему важно интегрировать различные программы CAD/CAM/CAE в единый рабочий процесс?", json.dumps(
                    {1: "Это создает излишнее дублирование данных",
                     2: "Позволяет эффективнее координировать рабочие процессы",
                     3: "Требуется меньше усилий для подготовки документации"}), 2),
                ("Какой фактор существенно замедляет внедрение инновационных технологий в крупные проекты?", json.dumps(
                    {1: "Страх перед новыми технологиями", 2: "Сложность интеграции существующих процессов",
                     3: "Недостаточно высокое качество программного обеспечения"}), 2),
                ("В чем проявляется польза регулярного обновления ПО в проектировании?", json.dumps(
                    {1: "Новые возможности повышают конкурентоспособность",
                     2: "Возникают постоянные технические сбои", 3: "Программы становятся менее интуитивными"}), 1)
            )

            DiagnosticModule.__init_questions(cursor, pol_first, 'POL', 1)
            DiagnosticModule.__init_questions(cursor, chl_first, 'CHL', 1)
            DiagnosticModule.__init_questions(cursor, umn_first, 'UMN', 1)

            DiagnosticModule.__init_questions(cursor, pol_second, 'POL', 2)
            DiagnosticModule.__init_questions(cursor, chl_second, 'CHL', 2)
            DiagnosticModule.__init_questions(cursor, umn_second, 'UMN', 2)

            DiagnosticModule.__init_questions(cursor, pol_third, 'POL', 3)
            DiagnosticModule.__init_questions(cursor, chl_third, 'CHL', 3)
            DiagnosticModule.__init_questions(cursor, umn_third, 'UMN', 3)

            DiagnosticModule.__init_results(cursor)
        except Exception as e:
            print(e)
            conn.rollback()
        finally:
            conn.commit()
            conn.close()

    @staticmethod
    def __init_student(cursor):
        cursor.execute('''
            INSERT INTO `Students`
            (`name`)
            VALUES (?);''', ('Иванов',))

    @staticmethod
    def __init_questions(cursor, questions, question_type, difficulty=1):
        insert = ((
            text,
            options,
            correct_answer,
            difficulty,
            question_type
        ) for text, options, correct_answer in questions)
        cursor.executemany('''
            INSERT INTO `Questions`
            (`text`, `options`, `correct_answer`, `difficulty`, `type`)
            VALUES (?, ?, ?, ?, ?);''', insert)

    @staticmethod
    def __init_results(cursor):
        results = (
            (1,  1, 'РД 1.1.',  '2025-09-01 12:00:00', 1, 1, 1, 0.6, 0.5, 0.3),
            (2,  1, 'РД 1.2.',  '2025-09-08 12:00:00', 1, 1, 1, 0.7, 0.5, 0.4),
            (3,  1, 'РД 1.3.',  '2025-09-15 12:00:00', 1, 1, 1, 0.8, 0.7, 0.3),
            (4,  1, 'РД 2.1.',  '2025-09-22 12:00:00', 1, 1, 1, 0.8, 0.8, 0.5),
            (5,  1, 'РД 2.2.',  '2025-09-29 12:00:00', 1, 1, 1, 0.9, 0.6, 0.2),
            (6,  1, 'РД 2.3.',  '2025-10-06 12:00:00', 1, 1, 1, 0.7, 0.5, 0.4),
            (7,  1, 'РД 2.4.',  '2025-10-13 12:00:00', 1, 1, 2, 0.6, 0.6, 0.3),
            (8,  1, 'РД 3.1.',  '2025-10-20 12:00:00', 1, 1, 2, 0.8, 0.7, 0.5),
            (9,  1, 'РД 3.2.',  '2025-10-27 12:00:00', 1, 1, 2, 0.9, 0.8, 0.6),
            (10, 1, 'РД 3.3.',  '2025-11-03 12:00:00', 1, 2, 1, 0.7, 0.7, 0.5),
            (11, 1, 'РД 4.1.',  '2025-11-10 12:00:00', 2, 2, 1, 0.6, 0.6, 0.4),
            (12, 1, 'РД 4.2.',  '2025-11-17 12:00:00', 2, 1, 2, 0.7, 0.7, 0.5),
            (13, 1, 'РД 4.3.',  '2025-11-24 12:00:00', 2, 2, 2, 0.8, 0.8, 0.6),
            (14, 1, 'РД 5.1.',  '2025-12-01 12:00:00', 2, 2, 2, 0.9, 0.8, 0.7),
            (15, 1, 'РД 5.2.',  '2025-12-08 12:00:00', 2, 2, 3, 0.8, 0.9, 0.6),
        )
        cursor.executemany('''
            INSERT INTO `Results`
            (`id`, `student_id`, `section`, `test_date`, `pol_c`, `chl_c`, `umn_c`, `pol`, `chl`, `umn`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''', results)

    def generate_test(self, question_type: str, difficulty: int) -> list[Question]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute(f'''
            SELECT * FROM `Questions` 
            WHERE `type`=? AND `difficulty`=? 
            ORDER BY RANDOM() LIMIT 3''',
                       (question_type, difficulty,))
        questions = [Question(q) for q in cursor.fetchall()]
        conn.close()

        return questions

    def get_additional_metric(self, student_id, metric, section) -> float:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT sum(pol), sum(chl), sum(umn) 
            FROM Results 
            WHERE `student_id`=? AND `section`=?
            GROUP BY `section`
            ''', (student_id, section))
        row = cursor.fetchone()
        if row is not None:
            metric_from_db = float(row[0 if metric == 'POL' else 1 if metric == 'CHL' else 2])
        else:
            metric_from_db = 0
        conn.close()
        return metric_from_db

    def save_results(self, student_id, section, pol_c, chl_c, umn_c, pol, chl, umn):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            '''
            INSERT INTO `Results`
            (`student_id`, `section`, `test_date`, `pol_c`, `chl_c`, `umn_c`, `pol`, `chl`, `umn`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''',
            (student_id, section, current_date, pol_c, chl_c, umn_c, pol, chl, umn,))

        conn.commit()
        conn.close()

    def display_student_results(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute("""
                SELECT student_id, section, s_complexity, pol, chl, umn 
                FROM Results
                ORDER BY student_id
            """)

        results = cursor.fetchall()
        conn.close()

        if not results:
            print("Нет данных в таблице Results")
            return

        student_data = defaultdict(list)
        for row in results:
            student_id, section, s_complexity, pol, chl, umn = row
            student_data[student_id].append({
                'section': section,
                's_complexity': s_complexity,
                'pol': pol,
                'chl': chl,
                'umn': umn
            })

        for student_id, records in student_data.items():
            print(f"\nSTUDENT ID: {student_id}")
            print("=" * 60)

            sections = [record['section'] for record in records]
            complexities = [record['s_complexity'] for record in records]
            pol_values = [f"{record['pol']:.1f}" if record['pol'] is not None else 'NULL' for record in records]
            chl_values = [f"{record['chl']:.1f}" if record['chl'] is not None else 'NULL' for record in records]
            umn_values = [f"{record['umn']:.1f}" if record['umn'] is not None else 'NULL' for record in records]

            def print_formatted_row(label, values, column_width=7):
                formatted_values = [f"{val:^{column_width}}" for val in values]
                print(f"{label:<10} | {' | '.join(formatted_values)}")

            print_formatted_row("Секция", sections)
            print_formatted_row("Сложность", complexities)
            print_formatted_row("POL", pol_values)
            print_formatted_row("CHL", chl_values)
            print_formatted_row("UMN", umn_values)

    def get_difficulties(self) -> dict[str, list[str]]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT type, GROUP_CONCAT(DISTINCT difficulty) as difficulties
            FROM Questions
            GROUP BY type
        ''')

        result = {}
        for row in cursor.fetchall():
            type_name = row[0]
            difficulties = set(map(int, row[1].split(','))) if row[1] else ()
            result[type_name] = difficulties

        conn.close()
        for k, v in result.items():
            result[k] = list(map(str, sorted(v)))
        return result

    def save_student(self, student_name) -> int:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO `Students`
            (`name`)
            VALUES (?)
            RETURNING id
            ''',
            (student_name,))

        student_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        return student_id

    def get_student_id_by_name(self, student_name):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT id FROM Students WHERE name = ?
            ''',
            (student_name,))

        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            return -1

    def get_all_students_have_result(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.`name` 
            FROM `Students` s
            WHERE EXISTS (
                SELECT 1 
                FROM `Results` r 
                WHERE r.`student_id` = s.`id` 
            )
            ORDER BY s.`name`
        """)
        results = cursor.fetchall()
        conn.close()
        return results

    def get_results_by_student_id(self, student_id):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute('''
                        SELECT section, pol_c, chl_c, umn_c, pol, chl, umn 
                        FROM Results 
                        WHERE student_id = ? 
                        ORDER BY id
                    ''', (student_id,))

        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        grouped_results = defaultdict(lambda: [0] * 6)
        result_counter = defaultdict(lambda: [0] * 3)
        for row in rows:
            r = Result(row)
            grouped_results[r.full_section][0] = max(r.pol_c, grouped_results[r.full_section][0])
            grouped_results[r.full_section][1] = max(r.chl_c, grouped_results[r.full_section][1])
            grouped_results[r.full_section][2] = max(r.umn_c, grouped_results[r.full_section][2])
            grouped_results[r.full_section][3] += r.pol
            grouped_results[r.full_section][4] += r.chl
            grouped_results[r.full_section][5] += r.umn
            result_counter[r.full_section][0] += 1 if r.pol != 0 or r.pol_c != 0 else 0
            result_counter[r.full_section][1] += 1 if r.chl != 0 or r.chl_c != 0 else 0
            result_counter[r.full_section][2] += 1 if r.umn != 0 or r.umn_c != 0 else 0

        results = []
        for section, metrics in grouped_results.items():
            r = Result([section] + [*metrics[:3]] +
                 [metrics[3] / result_counter[section][0] if result_counter[section][0] != 0 else metrics[3]] +
                 [metrics[4] / result_counter[section][1] if result_counter[section][1] != 0 else metrics[4]] +
                 [metrics[5] / result_counter[section][2] if result_counter[section][2] != 0 else metrics[5]])
            results.append(r)

        return results


if __name__ == "__main__":
    dm = DiagnosticModule()
    dm.display_student_results()
