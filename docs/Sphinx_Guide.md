# Генерация документации проекта через Sphinx

Инструкция предназначена для проекта из корня репозитория и пакетов `taskmanager` и `lab5_app`.
Для текущего проекта уже подготовлены `docs/source/conf.py` и `docs/source/index.rst`.

## Установка и настройка Sphinx

Установите Sphinx из корневого каталога проекта:

```powershell
python -m pip install sphinx
```

Для нового проекта `sphinx-quickstart --sep --project "Python console projects" --author "Student" docs`
создаёт конфигурацию в `docs/source/conf.py` и главную страницу в `docs/source/index.rst`.
В этом проекте эти файлы уже настроены, поэтому повторно запускать `sphinx-quickstart` не требуется.

## Настройка autodoc и Napoleon

В `docs/source/conf.py` уже добавлен корень репозитория в `sys.path` и включены расширения
`sphinx.ext.autodoc` и `sphinx.ext.napoleon`, чтобы извлекать API и читать Google-style докстринги:

```python
from pathlib import Path  # Импортируем Path для построения пути к корню проекта.
import sys  # Импортируем sys для добавления пути пакетов в список поиска импортов.
sys.path.insert(0, str(Path("../..").resolve()))  # Добавляем корень репозитория в путь импорта Python.
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]  # Включаем генерацию API и поддержку Google/reST докстрингов.
```

## Генерация страниц API

Из корневого каталога проекта сгенерируйте `.rst`-страницы для обоих пакетов:

```powershell
sphinx-apidoc -o docs/source/taskmanager taskmanager
sphinx-apidoc -o docs/source/lab5_app lab5_app
```

Файл `docs/source/index.rst` уже содержит `taskmanager/modules` и `lab5_app/modules` в директиве `toctree`.

## Сборка и просмотр HTML

Соберите документацию и откройте главную страницу в браузере:

```powershell
sphinx-build -b html docs/source docs/build/html
Start-Process docs/build/html/index.html
```

Если сборка сообщает о предупреждениях `autodoc`, сначала проверьте, что корень репозитория добавлен
в `sys.path`, расширения включены, а все документируемые объекты импортируются без ошибок.
