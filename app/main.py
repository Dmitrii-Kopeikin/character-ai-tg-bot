import logging

from fastapi import FastAPI

from app.amplitude_client import amplitude_client
from app.bot import CharacterAiBot
from app.database import Database
from app.redis import redis
from app.web import WebApp
from config import config


def init_logging() -> None:
    logging.basicConfig(
        filename="logs/bot.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


async def add_test_characters() -> None:
    from app.database.dal.character_dal import character_dal
    from app.database.test_data import TEST_DATA

    for character in TEST_DATA:
        await character_dal.create(**character)


def init_application() -> FastAPI:
    init_logging()
    # Init Databases.
    database = Database()
    # if config.debug.enabled:
    #     web.add_start_event_handler(add_test_characters)

    # Init FastAPI app.
    web = WebApp()
    web.add_start_event_handler(database.init_database)

    # Init CharacterAiBot
    character_ai_bot = CharacterAiBot(
        redis=redis,
        sessionmaker=database.sessionmaker,
    )

    web.add_start_event_handler(database.init_database)
    web.add_start_event_handler(character_ai_bot.init_webhook)
    web.add_start_event_handler(character_ai_bot.set_ui_commands)

    web.add_shutdown_event_handler(database.close)
    web.add_shutdown_event_handler(character_ai_bot.close)
    web.add_shutdown_event_handler(amplitude_client.shutdown)

    web.add_route(
        func=character_ai_bot.update,
        path=f"{config.bot.webhook_path}",
        method="POST",
    )

    return web.app


app = init_application()
