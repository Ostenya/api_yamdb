# YaMDb api (v1)


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Ostenya/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Как наполнить проект тестовыми данными (с удалением имеющихся):
```
python3 manage.py load_test_data
```
### Как наполнить проект тестовыми данными (без удаления имеющихся):
```
python3 manage.py load_test_data --no_delete
```



### Примеры запросов:
После запуска проекта примеры можно посмотреть [здесь](http://127.0.0.1:8000/redoc/).
