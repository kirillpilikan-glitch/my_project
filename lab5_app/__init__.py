"""Пакет консольного приложения для вычисления описательной статистики."""  # Докстринг кратко описывает назначение всего пакета.

__version__ = "1.0.0"  # Сохраняем версию пакета для использования в метаданных командной строки.

# Генерация документации выполняется из корневой папки проекта после установки Sphinx командой: pip install sphinx.
# Создайте раздельные каталоги исходников и сборки командой: sphinx-quickstart --sep --project "Lab 5" --author "Student" docs.
# Создайте страницы API для всех модулей пакета командой: sphinx-apidoc -o docs/source lab5_app.
# В docs/source/conf.py импортируйте sys и Path из pathlib, затем добавьте sys.path.insert(0, str(Path("../..").resolve())).
# Для настройки autodoc и Google-style докстрингов укажите в docs/source/conf.py: extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"].
# Добавьте modules в директиву toctree файла docs/source/index.rst, чтобы включить сгенерированный API-раздел в оглавление.
# Соберите HTML-документацию командой: sphinx-build -b html docs/source docs/build/html.
# Откройте готовую документацию в браузере из файла docs/build/html/index.html.
