import logging
from typing import Dict

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.chat_action import ChatActionMiddleware
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.utils.singleton_meta import SingletonMeta
from config import config

from .middlewares import AuthenticationMiddleware, DatabaseSessionMiddleware
from .routers import create_common_router, create_conversation_router

logger = logging.getLogger(__name__)


class CharacterAiBot(metaclass=SingletonMeta):
    def __init__(
        self,
        redis: Redis,
        sessionmaker: async_sessionmaker,
    ):
        self.bot = Bot(token=config.bot.token, parse_mode="HTML")

        storage = RedisStorage(redis=redis)

        self.dispatcher = Dispatcher(storage=storage, bot=self.bot)

        self.dispatcher.message.middleware(ChatActionMiddleware())

        self.dispatcher.update.middleware(
            DatabaseSessionMiddleware(session_pool=sessionmaker)
        )
        self.dispatcher.update.middleware(AuthenticationMiddleware())

        self.dispatcher.include_router(create_common_router())
        self.dispatcher.include_router(create_conversation_router())

    async def init_webhook(self):
        await self.bot.set_webhook(
            f"{config.server.host}{config.bot.webhook_path}"
        )

    async def update(
        self,
        update: Dict,
    ) -> None:
        try:
            telegram_update = types.Update(**update)
            await self.dispatcher.feed_update(
                bot=self.bot,
                update=telegram_update,
            )

            return {"success": True}
        except Exception as e:
            logger.error(e)
            return {"success": False}

    async def set_ui_commands(self):
        await self.bot.set_my_commands(
            commands=[
                types.BotCommand(
                    command="start",
                    description="Start",
                ),
                types.BotCommand(
                    command="menu",
                    description="Menu",
                ),
                types.BotCommand(
                    command="create_character",
                    description="Create Character",
                ),
            ],
        )

    async def send_message(self, text: str, chat_id: int):
        await self.bot.send_message(
            chat_id=chat_id,
            text=text,
        )

    async def close(self):
        await self.bot.close()
