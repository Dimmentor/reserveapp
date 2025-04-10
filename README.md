Асинхронное приложение для бронирования столиков. 
Стек: FastAPI, alembic, uvicorn, pytest, postrgesql


Запускаем сервис командой docker-compose up 

По команде запускаются контейнеры приложения, БД и тесты. Миграции уже применены.

Сервис так же включает: 

1)Обработка исключений: Конфликт записей на один столик и на одно временное окно, запись на несуществующий столик.

2)Тесты на все CRUD сценарии.

При необходимости можно подключиться к БД и сделать SQL-запросы для проверки:

docker exec -it reserveappdb psql -U reserveapp -d reserveapp

SELECT * FROM tables;

SELECT * FROM reservations;


Примеры API-запросов(Указываем даты в формате ISO 8601):
1)	Создание столиков

POST http://localhost:5050/tables/

Тело запроса: 

{    
  "name": "Столик 1",
  "seats": 4,
  "location": "Первый этаж"
}

2)	Получение всех столиков
GET http://localhost:5050/tables/

3)	Создание бронирования
POST http://localhost:5050/reservations/

Тело запроса: 

{    
  "customer_name": "Дмитрий ",    
  "table_id": 1,
  "reservation_time": "2025-10-01T18:00:00",
  "duration_minutes": 60
}

4)	Проверка на конфликт записей
POST http://localhost:5050/reservations/

Тело запроса: 

{    
  "customer_name": "Иван",    
  "table_id": 1,
  "reservation_time": "2025-10-01T18:30:00",
  "duration_minutes": 60
}

5)	Получение всех бронирований 
GET http://localhost:5050/reservations/

6)	Удаление бронирований по id 
DELETE http://localhost:5050/reservations/{id}

7)	Удаление столиков по id 
DELETE http://localhost:5050/tables/{id}
