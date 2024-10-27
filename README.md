# TrueMatch

Сервис знакомств на FastApi. Состоит из следующих эндпоинтов:

- Эндпоинт для регистрации нового участника:
  - URL: /api/clients/create
  
  При регистрации нового участника на его аватарку накладывается водяной знак.
  Наложение выполняется через брокер задач, не блокируя основной поток выполнения.
- Эндпоинт авторизации:
  - URL: /api/clients/login
  
  При успешной авторизации создается JWT токен.
- Эндпоинт логаута:
  - URL: /api/clients/logout
  
  JWT токен удаляется.
- Эндпоинт оценивания участником другого участника:
  - URL: /api/clients/{id}/match

  Если у пользователей возникает взаимная симпатия, то обоим высылается почта другого участника 
  на email с сообщением вида: «Вы понравились <имя>! Почта участника: <почта>». 
- Эндпоинт для получения списка участников:
  - URL: /api/list
  
  Доступна фильтрация по полу, имени, фамилии, дате регистрации и расстоянию относительно авторизованного пользователя.
  Значения расстояний между пользователями кэшируются, для улучшения производительности.

## Стек
- FastApi
- PostgreSQL
- Redis
- Celery
- Docker

## Подготовка к установке

В корне проекта создайте '.env' файл с переменными окружения.
Пример файла `.env-prod-example':

```
DAILY_LIKES_LIMIT=10
AVATARS_DIR="app/static/avatars/"
WATERMARK_PATH="app/static/watermark.png"

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=root
DB_NAME=postgres

POSTGRES_DB=true_match_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

ENCRYPTION_KEY=s3XUjyntOk0o=
JWT_SECRET_KEY=asdlajsdasASDASD=
ALGORITHM=HS256
ORIGINS=["http://127.0.0.1:8000", "http://127.0.0.1:3000"]

REDIS_HOST=localhost
REDIS_PORT=6379

SMTP_HOST=smtp.mail.com
SMTP_USER=mymail@mail.com
SMTP_PASSWORD=password
SMTP_PORT=465
```
где:

- `DAILY_LIKES_LIMIT` лимит лайков в сутки, по умолчанию 10
- `AVATARS_DIR` путь к директории с аватарами пользователей, по умолчанию **app/static/avatars/**
- `WATERMARK_PATH` путь к изображению водяного знака, по умолчанию **app/static/watermark.png**
- `DB_HOST` адрес БД, по умолчанию 'localhost'
- `DB_PORT` порт БД, по умолчанию '5432'
- `DB_USER` пользователь БД, по умолчанию 'postgres'
- `DB_PASS` пароль БД, по умолчанию 'root'
- `DB_NAME` название БД, по умолчанию 'postgres'
- `ENCRYPTION_KEY` ключ для шифрования паролей пользователей, нет значения по умолчанию
- `JWT_SECRET_KEY` ключ для генерации JWT-токена, нет значения по умолчанию
- `ALGORITHM` алгоритм для шифрования JWT-токена, по умолчанию 'HS256'
- `JWT_TOKEN_DELAY_MINUTES` время жизни JWT-токена в минутах, по умолчанию 30
- `ORIGINS` список разрешенных адресов для работы с API, по умолчанию '["http://127.0.0.1:8000", "http://127.0.0.1:3000"]'
- `REDIS_HOST` адрес redis, по умолчанию 'localhost'
- `REDIS_PORT` порт redis, по умолчанию '6379'
- `SMTP_HOST` хост почтового сервера, нет значения по умолчанию
- `SMTP_USER` адрес почты, для подключения к серверу, нет значения по умолчанию
- `SMTP_PASSWORD` пароль, для подключения к почтовому серверу, нет значения по умолчанию
- `SMTP_PORT` порт почтового сервера, нет значения по умолчанию

Замените в файле `docker-compose.yml` название `.env` файла на свое.

## Запуск приложения

Скачайте код:

```
git clone https://github.com/free-flow-code/TrueMatch.git
```

Установите Docker и Docker-compose. [Ссылка на инструкцию](https://www.howtogeek.com/devops/how-to-install-docker-and-docker-compose-on-linux/).

Перейдите в директорию проекта запустите docker-compose:

```
docker compose up --build
```

Сайт будет доступен по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Flower доступен по адресу [http://127.0.0.1:5555/](http://127.0.0.1:5555).