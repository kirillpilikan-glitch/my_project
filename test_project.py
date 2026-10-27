"""Автоматические проверки модели, SQLite-хранилища и команд приложения."""  # Докстринг описывает набор модульных тестов проекта.

import contextlib  # Импортируем средства временного перенаправления вывода в тестах CLI.
import io  # Импортируем буфер для проверки напечатанных сообщений.
import sqlite3  # Импортируем SQLite для дополнительных проверок состояния базы.
import tempfile  # Импортируем создание изолированных временных каталогов для тестовых БД.
import unittest  # Импортируем стандартную библиотеку модульного тестирования.
from contextlib import closing  # Импортируем помощник для гарантированного закрытия тестового соединения SQLite.
from pathlib import Path  # Импортируем Path для адреса тестовой базы.

from taskmanager.main import main  # Импортируем точку входа CLI для тестов командной строки.
from taskmanager.models import Task  # Импортируем модель для проверки правил данных.
from taskmanager.storage import add_task, delete_task, list_tasks, update_task  # Импортируем операции SQLite для изолированных тестов.
from lab5_app.cli import main as statistics_main  # Импортируем точку входа статистического CLI для проверки второго пакета.
from lab5_app.statistics import calculate_statistics  # Импортируем расчёт статистики для модульных тестов.


class TaskModelTests(unittest.TestCase):  # Группируем тесты проверки модели задачи.
    """Проверяет валидацию и методы модели Task."""  # Докстринг описывает назначение тестового класса.

    def test_task_defaults_and_completion(self) -> None:  # Проверяем значения по умолчанию и завершение задачи.
        """Проверяет создание задачи и переход в статус done."""  # Докстринг описывает проверяемое поведение.
        task = Task(id=1, title="Проверка")  # Создаём задачу с обязательными полями и значениями по умолчанию.
        completed = task.mark_done()  # Создаём копию задачи в завершённом состоянии.
        self.assertEqual(task.status, "todo")  # Проверяем, что исходная задача осталась незавершённой.
        self.assertEqual(completed.status, "done")  # Проверяем, что копия задачи отмечена выполненной.
        self.assertTrue(completed.created_at)  # Проверяем, что время создания было заполнено автоматически.
        self.assertNotEqual(id(task), id(completed))  # Проверяем, что завершение создало отдельный объект.

    def test_invalid_task_values_raise_value_error(self) -> None:  # Проверяем отказ модели принимать недопустимые поля.
        """Проверяет исключение для пустого названия и неверного приоритета."""  # Докстринг описывает проверяемые ошибки.
        with self.assertRaises(ValueError):  # Требуем ValueError для пустого названия задачи.
            Task(id=1, title="   ")  # Пытаемся создать задачу без видимого названия.
        with self.assertRaises(ValueError):  # Требуем ValueError для приоритета вне диапазона.
            Task(id=1, title="Ошибка", priority=6)  # Пытаемся создать задачу с недопустимым приоритетом.
        with self.assertRaises(ValueError):  # Требуем ValueError для неизвестного статуса.
            Task(id=1, title="Ошибка", status="unknown")  # Пытаемся создать задачу с неподдерживаемым состоянием.


class SQLiteStorageTests(unittest.TestCase):  # Группируем тесты хранения и изменения записей SQLite.
    """Проверяет создание, фильтрацию, завершение и удаление задач в SQLite."""  # Докстринг описывает область тестирования класса.

    def setUp(self) -> None:  # Создаём новую временную базу перед каждым тестом.
        """Создаёт временную директорию и путь к тестовой БД."""  # Докстринг описывает подготовку тестового окружения.
        self.temporary_directory = tempfile.TemporaryDirectory()  # Создаём изолированное временное хранилище для теста.
        self.database_path = Path(self.temporary_directory.name) / "tasks.sqlite3"  # Задаём путь SQLite-файла внутри временного каталога.

    def tearDown(self) -> None:  # Удаляем временную базу после завершения каждого теста.
        """Освобождает временный каталог теста."""  # Докстринг описывает очистку тестовых данных.
        self.temporary_directory.cleanup()  # Удаляем только временную папку, принадлежащую текущему тесту.

    def test_add_and_filter_tasks(self) -> None:  # Проверяем вставку данных и SQL-фильтры.
        """Проверяет добавление задач и фильтрацию по статусу и приоритету."""  # Докстринг описывает проверяемое поведение.
        first = add_task(self.database_path, "Первая задача", "Описание", priority=1)  # Добавляем задачу высокого приоритета.
        add_task(self.database_path, "Вторая задача", priority=3)  # Добавляем вторую задачу с обычным приоритетом.
        self.assertEqual(first.id, 1)  # Проверяем, что первая запись получила начальный ID SQLite.
        self.assertEqual(len(list_tasks(self.database_path)), 2)  # Проверяем, что база содержит обе созданные задачи.
        self.assertEqual([task.title for task in list_tasks(self.database_path, priority=1)], ["Первая задача"])  # Проверяем фильтрацию записей по приоритету.

    def test_update_and_delete_task(self) -> None:  # Проверяем изменение статуса и удаление записи.
        """Проверяет сохранение статуса done и удаление выбранной задачи."""  # Докстринг описывает проверяемые SQL-операции.
        task = add_task(self.database_path, "Завершить отчёт")  # Создаём задачу для последующего обновления.
        updated = update_task(self.database_path, task.id, done=True)  # Меняем её статус на выполненный.
        self.assertEqual(updated.status, "done")  # Проверяем возвращаемое состояние обновлённой задачи.
        self.assertEqual(list_tasks(self.database_path, status="done"), [updated])  # Проверяем запись статуса и фильтр в базе.
        deleted = delete_task(self.database_path, task.id)  # Удаляем задачу и получаем удалённую модель.
        self.assertEqual(deleted.id, task.id)  # Проверяем идентификатор удалённой записи.
        self.assertEqual(list_tasks(self.database_path), [])  # Проверяем, что список задач после удаления пуст.

    def test_missing_task_raises_key_error(self) -> None:  # Проверяем ошибки для неизвестного идентификатора.
        """Проверяет, что обновление и удаление отсутствующей задачи вызывают KeyError."""  # Докстринг описывает проверяемое исключение.
        with self.assertRaises(KeyError):  # Требуем KeyError при обновлении несуществующей записи.
            update_task(self.database_path, 999, done=True)  # Пытаемся завершить задачу, которой нет в базе.
        with self.assertRaises(KeyError):  # Требуем KeyError при удалении несуществующей записи.
            delete_task(self.database_path, 999)  # Пытаемся удалить задачу, которой нет в базе.

    def test_sql_injection_text_is_stored_as_data(self) -> None:  # Проверяем параметризацию SQL для пользовательского заголовка.
        """Проверяет сохранение SQL-подобного текста без выполнения как команды."""  # Докстринг описывает проверку безопасной передачи значений.
        title = "Задача'); DROP TABLE tasks; --"  # Задаём заголовок, который не должен интерпретироваться как SQL.
        task = add_task(self.database_path, title)  # Передаём текст в параметризованный INSERT.
        self.assertEqual(list_tasks(self.database_path)[0].title, title)  # Проверяем, что строка сохранена без изменений.
        with closing(sqlite3.connect(self.database_path)) as connection:  # Открываем базу и гарантируем закрытие соединения.
            table = connection.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'tasks'").fetchone()  # Ищем таблицу tasks системным запросом SQLite.
        self.assertIsNotNone(table)  # Проверяем, что пользовательский текст не удалил таблицу.
        self.assertEqual(task.title, title)  # Проверяем, что возвращённая модель содержит исходный текст.


class CommandLineTests(unittest.TestCase):  # Группируем проверки пользовательских CLI-команд.
    """Проверяет исполнение команд через argparse и работу вывода."""  # Докстринг описывает назначение тестового класса.

    def test_add_and_list_commands(self) -> None:  # Проверяем, что CLI создаёт запись и показывает её.
        """Проверяет успешное добавление задачи и вывод списка."""  # Докстринг описывает последовательность CLI.
        with tempfile.TemporaryDirectory() as directory:  # Создаём временную директорию для файла базы CLI.
            database = str(Path(directory) / "cli.sqlite3")  # Формируем путь к изолированному файлу SQLite.
            with contextlib.redirect_stdout(io.StringIO()) as add_output:  # Перехватываем консольный вывод команды добавления.
                add_result = main(["--add", "CLI задача", "--database", database])  # Запускаем CLI для создания записи в тестовой базе.
            self.assertEqual(add_result, 0)  # Проверяем код успешного выполнения добавления.
            self.assertIn("CLI задача", add_output.getvalue())  # Проверяем подтверждение создания задачи.
            with contextlib.redirect_stdout(io.StringIO()) as list_output:  # Перехватываем консольный вывод команды списка.
                list_result = main(["--list", "--database", database])  # Запускаем CLI для чтения сохранённых записей.
            self.assertEqual(list_result, 0)  # Проверяем код успешного выполнения вывода списка.
            self.assertIn("CLI задача", list_output.getvalue())  # Проверяем наличие задачи в результате чтения.


class StatisticsTests(unittest.TestCase):  # Группируем проверки статистического пакета Лабораторной работы № 5.
    """Проверяет расчёт статистики и запуск второго консольного приложения."""  # Докстринг описывает область проверки класса.

    def test_statistics_for_numbers(self) -> None:  # Проверяем вычисление основных показателей набора чисел.
        """Проверяет количество, сумму, среднее, медиану, минимум и максимум."""  # Докстринг описывает проверяемый результат.
        result = calculate_statistics([1.0, 2.0, 3.0])  # Вычисляем показатели для заранее известной последовательности.
        self.assertEqual(result, {"count": 3, "sum": 6.0, "mean": 2.0, "median": 2.0, "min": 1.0, "max": 3.0})  # Сверяем полный словарь статистических результатов.

    def test_empty_or_non_finite_data_raises_value_error(self) -> None:  # Проверяем отклонение пустых и не конечных наборов.
        """Проверяет ValueError для пустой последовательности и бесконечности."""  # Докстринг описывает ожидаемые ошибки расчёта.
        with self.assertRaises(ValueError):  # Требуем ValueError для пустых входных данных.
            calculate_statistics([])  # Передаём пустой список, для которого статистика не определена.
        with self.assertRaises(ValueError):  # Требуем ValueError для не конечных значений.
            calculate_statistics([1.0, float("inf")])  # Передаём бесконечность для проверки валидации.

    def test_statistics_cli_prints_results(self) -> None:  # Проверяем вывод и код завершения CLI статистики.
        """Проверяет запуск argparse-интерфейса с набором чисел."""  # Докстринг описывает сценарий запуска.
        with contextlib.redirect_stdout(io.StringIO()) as output:  # Перехватываем консольный вывод, чтобы проверить его содержимое.
            result = statistics_main(["1", "2", "3"])  # Запускаем приложение с тремя позиционными числовыми аргументами.
        self.assertEqual(result, 0)  # Проверяем код успешного завершения приложения.
        self.assertIn("Количество: 3", output.getvalue())  # Проверяем, что CLI вывел количество чисел.
        self.assertIn("Сумма: 6", output.getvalue())  # Проверяем, что CLI вывел корректную сумму.


if __name__ == "__main__":  # Проверяем, запущен ли этот тестовый файл непосредственно.
    unittest.main()  # Запускаем стандартный тестовый runner при запуске python test_project.py.
