# 😺 [QRKot](https://github.com/KomkovAleksey/QRkot_spreadsheets)


## Оглавление

- [Автор](#Автор)
- [Технологии](#технологии)
- [Описание проекта](#Описание-проекта)
- [Права пользователей](#Права-пользователей)
- [Установка и запуск проекта](#установка-и-запуск-проекта)
- [Примеры запросов к API](#Примеры-запросов-к-API)

## Технологии:

- Python 3.9.10
- Fastapi 0.78.0
- SQLalchemy 1.4.36
- Alembic 1.7.7
- Uvicorn 0.17.6
- Google API

## Описание проекта:

Приложение для Благотворительного фонда поддержки котиков QRKot.

Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект.

Может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.

## Права пользователей:

Любой пользователь может видеть список всех проектов, включая требуемые и уже внесенные суммы. Это касается всех проектов — и открытых, и закрытых.
### Авторизованный пользователь может:
Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований.
### Неавторизованный пользователь может:

Получить список всех проектов.

### Суперпользователь может:
Создавать проекты, удалять проекты, в которые не было внесено средств,
изменять название и описание существующего проекта, устанавливать для него новую требуемую сумму (но не меньше уже внесённой).

## Установка и запуск проекта

### Запуск проекта:

* Клонируйте репозиторий и перейдите в него в командной строке:
```
mkdir cat_charity_fund
```
```
cd cat_charity_fund
```
```
git clone https://github.com/KomkovAleksey/cat_charity_fund
```
Cоздайте и активируйте виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

* Установите зависимости из файла requirements.txt и обновите pip:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

* Создайте .env файл в корневой папке проекта. 
```
touch .env
```
В нем должны быть указаны. 
```
DATABASE_URL=
SECRET=
APP_TITLE=
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
# Данные вашего сервисного аккаунта
TYPE=
PROJECT_ID=
PRIVATE_KEY_ID=
PRIVATE_KEY=
CLIENT_EMAIL=
CLIENT_ID=
AUTH_URI=
TOKEN_URI=
AUTH_PROVIDER_X509_CERT_URL=
CLIENT_X509_CERT_URL=
EMAIL=
```
В корневой папке есть файл .env.example,
с примером того как надо заполнять .env файл.
### Запуск проекта:
Применить миграции:
```
alembic upgrade head
```
Запустить проект:
```
uvicorn app.main:app
```
Сервис QRKot будет доступен по адресу: http://127.0.0.1:8000


## Примеры запросов к API
Все запросы делались в приложении [Postman](https://www.postman.com/)

POST charity_project

http://127.0.0.1:8000/charity_project/
```
{
    "name": "string",
    "description": "string",
    "full_amount": 0
}
```
Ответ
```
{
    "name": "string",
    "description": "string",
    "full_amount": 0,
    "id": 0,
    "invested_amount": 0,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
}
```
Создание пожертвования

POST donation

http://127.0.0.1:8000/donation/
```
{
    "full_amount": 0,
    "comment": "string"
}
```
Ответ
```
{
    "full_amount": 0,
    "comment": "string",
    "id": 0,
    "create_date": "2019-08-24T14:15:22Z"
}
```
Регистрация пользователя

POST user

http://127.0.0.1:8000/auth/register
```
{
    "email": "{{firstUserEmail}}",
    "password": "{{firstUserPassword}}"
}
```
Ответ
```
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
```

## Автор

[Алексей Комков](https://github.com/KomkovAleksey)
