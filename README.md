# async_file_uploader

![Static Badge](https://img.shields.io/badge/Python-FFD43B?logo=python&logoColor=blue) 
![Static Badge](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=green)
![Static Badge](https://img.shields.io/badge/celery-%2337814A.svg?logo=celery&logoColor=white)
![Static Badge](https://img.shields.io/badge/redis-%23DC382D.svg?logo=redis&logoColor=white)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
![code style](https://img.shields.io/badge/code%20style-black-000000.svg)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## Описание проекта
АПИ с эндпоинтом для массовой загрузки файлов с обработкой в фоне и WebSocket-уведомлениями.

## Предварительные условия
На компьютере должны быть установлены:
- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation) для работы с зависимостями
- [Postman](https://www.postman.com/) для проверки работоспособности

## Создание виртуального окружения в Poetry и установка зависимостей

```
poetry init  # указываем версию python3.12 и заполняем остальные поля pyproject.toml
poetry env use /usr/bin/python3.12  # используем python3.12 для создания виртуального окружения вместо дефолтной версии питона в системе
poetry install  # установить зависимости из файла poetry.lock
```

## Запуск без Docker
Создать в папке src/config файл с названием ".env" и следующим содержанием:

```
SECRET_KEY=key
MODE=dev
CELERY_BROKER=redis://127.0.0.1:6379
CELERY_BACKEND=redis://127.0.0.1:6379
```

Открыть 3 терминала:
- в первом запустить redis-server;
- во втором активировать виртуальное окружение командой poetry shell, выполнить миграции 
(make migrate, если у вас Ubuntu и установлена утилита make для работы Makefile, либо из папки src 
выполнить команду python3 manage.py migrate) и 
запустить основное Django-приложение через uvicorn (make uvicorn, если у вас Ubuntu и установлена утилита make для работы Makefile, либо из папки src выполнить команду uvicorn config.asgi:application --reload);
- в третьем активировать виртуальное окружение командой poetry shell и 
запустить celery worker (make celery-worker, если у вас Ubuntu и установлена утилита make для работы Makefile,  
либо перейти из папки src выполнить команду python3 -m celery -A config.celery.app worker -l info).

## Получение WebSocket-уведомлений через Postman
- Нажать в Postman кнопку New, выбрать WebSocket. В поле URL вставить ссылку типа 
ws://127.0.0.1:8000/ws/upload/<название_ws_channel_на_ваш_выбор>/
и нажать на кнопку Connect.
- Откроется подключение к этому ws_channel.
- Теперь можно выполнить запрос к апи-эндпойнту http://127.0.0.1:8000/api/upload/ (см. следующий шаг).
- При работе апи WebSocket-уведомления оттображаются в разделе Response, нужно выбрать Received Messagesв в выпадающем списке.

## Апи-запрос в Postman с загрузкой нескольких файлов
- В Postman создать http POST-запрос на URL http://127.0.0.1:8000/api/upload/
- Для отправки на эндпойнт нескольких файлов нужно в разделе body выбрать form-data и создать ключ с именем files и типом file, а в поле value загрузить файлы с локального компьютера, но выбрать не один файл, а несколько с помощью клавиш Ctrl или Shift.
То есть ключ files один, но к нему привязано несколько файлов.
- Также добавить ключ ws_channel типа text, в value вставить ваше название ws_channel.
То есть на прошлом шаге мы подключались к вебсокету по ссылке ws://127.0.0.1:8000/ws/upload/<название_ws_channel_на_ваш_выбор>/, 
и сейчас в value ключа ws_channel нужно вставить то, что вы указали вместо <название_ws_channel_на_ваш_выбор> в этой ссылке.

## Где хранятся загруженные файлы
В папке src/media/uploads/
