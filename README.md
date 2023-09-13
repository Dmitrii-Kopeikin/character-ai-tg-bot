# Character AI Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.0.0-blue)](https://docs.aiogram.dev/en/latest/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-blue)](https://fastapi.tiangolo.com/)
[![Redis](https://img.shields.io/badge/Redis-latest-blue)](https://redis.io/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.20-blue)](https://www.sqlalchemy.org/)
[![Postgres](https://img.shields.io/badge/Postgres-latest-blue)](https://www.postgres.org/)
[![httpx](https://img.shields.io/badge/httpx-0.25.0-blue)](https://www.python-httpx.org/)
[![pydantic](https://img.shields.io/badge/pydantic-2.1.1-blue)](https://www.pydantic.dev/)
[![amplitude](https://img.shields.io/badge/amplitude-1.1.3-blue)](https://www.amplitude.com/)

## Описание

Character AI Telegram Bot - это Telegram-бот, который может пообщаться с тобой от лица какого-нибудь персонажа или известной личности.

Данный бот разрабатывался как тестовое задание. Его функционал пока ограничен.
Вы можете выбирать личность для бота и вести с ним беседу.

## Функции

-   Выбор личности
-   Запросы, вопросы и т.д.

## Использованные технологии

-   Python 3.11
-   [Aiogram](https://docs.aiogram.dev/en/latest/) - Python-фреймворк для создания Telegram-ботов
-   [FastAPI](https://fastapi.tiangolo.com/) - Python-фреймворк для создания веб-приложений с высокой производительностью
-   [Uvicorn](https://www.uvicorn.org/) - ASGI-сервер, используемый для запуска FastAPI
-   [SQLAlchemy](https://www.sqlalchemy.org/) - Python-библиотека для работы с реляционными базами данных
-   [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Python-библиотека для миграции баз данных
-   [httpx](https://www.python-httpx.org/) - Python-библиотека для выполнения HTTP-запросов
-   [Redis](https://redis.io/) - In-memory база данных с открытым исходным кодом

## Установка

В первую очередь необходимо зарегистрировать бота в сети Telegram и получить токен. Для этого можно воспользоваться ботом @BotFather.

Данный бот использует Telegram Hook. Следовательно для его запуска нужен белый IP, или можно использовать утилиту и сервис https://ngrok.com.

Перед запуском необходимо переименовать файл '.env.template' в '.env' и заполнить в нем все переменные.

## Запуск

Для быстрого запуска можно использовать команду docker-compose up.


## Использование

При вводе команды /start происходите регистрация пользователя и появляется кнопка выбора личности для бота.
Личность можно сменить в любой момент с помощью команды /menu.
