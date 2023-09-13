from aiogram import Router
from aiogram.filters import Command, CommandStart

from ..handlers.commands import menu_handler, start_handler


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

    return router
