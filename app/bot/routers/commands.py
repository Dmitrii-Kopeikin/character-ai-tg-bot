from aiogram import Router
from aiogram.filters import Command, CommandStart

from ..handlers.commands import (
    create_character_handler,
    menu_handler,
    start_handler,
)


def create_common_router() -> Router:
    router = Router()

    router.message.register(
        start_handler,
        CommandStart(),
    )

    router.message.register(
        menu_handler,
        Command(commands=["menu"]),
    )

    router.message.register(
        create_character_handler,
        Command(commands=["create_character"]),
    )

    return router
