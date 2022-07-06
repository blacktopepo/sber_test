Формат выгрузки в csv файл похож на тот что мы видим на сайте.

Выгрузка в БД происходит в таблицу вида:
```
имя региона | год | значение
```
Переменные окружения для БД:
```
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
```

Зависимости для приложения в файле requirements.txt, установка:
```
pip install -r requirements.txt
```
Запуск приложения:
```
python app/main.py
```
