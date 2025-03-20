# async_file_uploader

## Создание виртуального окружения в Poetry

```
poetry init  # указываем версию python3.12 и заполняем остальные поля pyproject.toml
poetry env use /usr/bin/python3.12  # используем python3.12 для создания виртуального окружения вместо дефолтной версии питона в системе
poetry install  # установить зависимости из файла poetry.lock
```

## Запуск без Docker
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
Нажать в Postman кнопку New, выбрать WebSocket. В поле URL вставить ссылку типа 
ws://127.0.0.1:8000/ws/upload/<название_ws_channel_на_ваш_выбор>/
и нажать на кнопку Connect.
Откроется подключение к этому ws_channel.
После этого можно выполнять запрос к апи-эндпойнту http://127.0.0.1:8000/api/upload/ и 
видеть в ответ WebSocket-уведомления на вкладке Postman с этим подключенным ws_channel в разделе 
Response, выбрав Received Messagesв в выпадающем списке.

## Апи-запрос в Postman с загрузкой нескольких файлов
В Postman создать http POST-запрос на URL http://127.0.0.1:8000/api/upload/
При этом в разделе body выбрать form-data и создать ключ с именем files и типом file, а в поле value загрузить файлы с 
локального компьютера, но выбрать не один файл, а несколько с помощью клавиш Ctrl или Shift.
То есть ключ files один, но к нему привязано несколько файлов.
Добавить также ключ ws_channel типа text, в value вставить ваше название ws_channel.
То есть на прошлом шаге мы подключались к вебсокету по ссылке ws://127.0.0.1:8000/ws/upload/<название_ws_channel_на_ваш_выбор>/, 
значит сейчас в value ключа ws_channel надо вставить то, что вы написали вместо <название_ws_channel_на_ваш_выбор> в этой ссылке.

## Где хранятся загруженные файлы
В папке src/media/uploads/
