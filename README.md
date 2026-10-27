# Учебный проект по Python

В репозитории собраны лабораторные работы и консольные приложения по курсу Python.
Исходные задания находятся в PDF-файлах в корне проекта.

## Основные файлы и пакеты

- `Laba 1.py` — условия, циклы, числа и строки.
- `Laba 2.py` — циклы, списки, словари, множества и комбинированные упражнения.
- `Laba 3.py` — comprehensions, итератор, генератор, `Decimal`, `fractions` и `datetime`.
- `Laba 4.py` — наследование, магические методы и полиморфизм.
- `Practice 2.py` — декораторы логирования и проверки роли.
- `taskmanager/` — CLI-менеджер задач с хранением в SQLite.
- `lab5_app/` — CLI-приложение статистики.
- `test_project.py` — автоматические тесты через `unittest`.
- `docs/` — руководство и сгенерированная Sphinx HTML-документация.

## Запуск

Используйте Python 3.10 или новее. Команды запускаются из корня проекта:

```powershell
python "Laba 1.py"
python "Laba 2.py"
python "Laba 3.py"
python "Laba 4.py"
python "Practice 2.py"
python main.py --help
python -m lab5_app 1 2 3
```

Для создания API-страниц и сборки документации установите Sphinx и выполните:

```powershell
python -m pip install sphinx
sphinx-apidoc --force -o docs/source/taskmanager taskmanager
sphinx-apidoc --force -o docs/source/lab5_app lab5_app
sphinx-build -b html docs/source docs/build/html
```

Откройте `docs/build/html/index.html` для просмотра документации.

## Тесты

Запустите тестовый набор командой:

```powershell
python -m unittest -v test_project
```
