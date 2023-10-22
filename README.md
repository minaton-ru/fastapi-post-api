# API приложение для скачивания и сохранения вопросов для викторины  

Приложение запрашивает с API сервиса jService случайные вопросы для викторины, сохраняет их в базу данных.  

## Функционал  
Ендпойнт принимает запрос POST, в котором указывается количество вопросов для скачивания.  Запрашивает с сервиса jService указанное количество вопросов. Сохраняет в базу данных все полученные вопросы. Если среди полученных вопросов есть уже существующий в базе данных, то на сервис jService отправляется дополнительный запрос на получение нового вопроса, до тех пор, пока не будет получен уникальный.   
В ответ на POST-запрос возвращается предыдущий сохраненный в БД вопрос.    
Когда в локальной БД будет 221510 записей, сервис будет возвращать ошибку 406, потому что скачаны все вопросы из jService.  
Запрашивать в POST-запросе больше 100 за один раз нет смысла, потому что в jService ограничени на 100 вопросов.  
  
## Стек  
Python  
FastAPI  
aiohttp  
alembic  
SQLAlchemy    
  
## Структура данных

Модель Question:  
- id = primary_key
- answer = текст ответа  
- question = текст вопроса  
- category_id = номер категории  
- loaded_at = дата и время сохранения в локальную БД  
- created_at = дата и время создания  
- updated_at = дата и время изменения  

## Описание API  

В проекте есть документация Swagger, доступная после запуска приложения по адресу `http://127.0.0.1/docs/`  

### Запрос

На ендпойнт `/api/question/` отправляется POST-запрос вида:
```
POST /robots/create/ HTTP/1.1
Host: 127.0.0.1
Content-Type: application/json

{"questions_num": N}
```

Где:  
- N - число вопросов    

### Ответ  

Если данные в запросе валидны, то ендпойнт вернет ответ 201 CREATED и данные с предыдущим сохраненным вопросом:
```
HTTP 201 CREATED
Content-Type: application/json
Date:
Server: uvicorn
Content-Length:    

Body:  

[
    {
        "category_id": 9537,
        "loaded_at": "2023-10-22T17:48:02.106598",
        "question": "(Her Majesty delivers the clue again.) In 2007 UNICEF Canada supplied 33,000 insecticide-treated bednets to help children & pregnant women in Liberia to fight this disease",
        "id": 122525,
        "answer": "malaria",
        "created_at": "2022-12-30T19:57:50.557000",
        "updated_at": "2022-12-30T19:57:50.557000"
    }
]
``` 

## Установка  

1. Скопировать файлы:  
```
$ git clone https://github.com/minaton-ru/fastapi-post-api.git
```
2. Создать файл `.env` для переменных окружения. Пример файла:
```
DATABASE_PORT=5432
POSTGRES_PASSWORD=password1
POSTGRES_USER=postgresuser
POSTGRES_DB=question
POSTGRES_HOST=database
POSTGRES_HOSTNAME=127.0.0.1
```
3. Сборка образа и запуск контейнеров:  
```
docker-compose up --build
```

4. Открыть в браузере URL c Swagger-документацией  `http://127.0.0.1/docs/`, указать количество вопросов и сделать тестовый запрос.
5. Или через Postman отправить POST-запросы с помощью коллекции [fastapi-post-api.postman_collection.json](fastapi-post-api.postman_collection.json).  

## TODO  

- Добавить тесты  
- Добавить логирование   