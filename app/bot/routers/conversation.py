from aiogram import Router

from ..filters import IsNotCommand
from ..handlers.conversation import message_handler


def create_conversation_router() -> Router:
    router = Router()

    router.message.register(
        message_handler,
        IsNotCommand(),
    )

    return router
