import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.dal import user_dal
from app.database.models import User
from app.amplitude_client import amplitude_client

logger = logging.getLogger("AuthenticationMiddleware")


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if event.event_type == "callback_query":
            callback_query: CallbackQuery = event.event
            message: Message = callback_query.message
            user_tg_id = callback_query.from_user.id
        else:
            message: Message = event.event
            user_tg_id = message.from_user.id

        session = data["session"]
        user = await user_dal.get(tg_id=user_tg_id, session=session)
        if not user:
            logger.info(f"Registering new user: {user_tg_id}")
            user = await self.process_first_visit(
                user_tg_id=user_tg_id, session=session
            )
            amplitude_client.track_registration(
                user_id=user.id,
                data={
                    "user_tg_id": user_tg_id,
                    "locale": user.locale,
                },
            )
            logger.info(f"Registration of user {user_tg_id} successful.")
        else:
            await user_dal.update(user.id, session=session)

        # Injecting user_id (not telegram user ID!):
        data["user_id"] = user.id

        return await handler(event, data)

    async def process_first_visit(
        self,
        user_tg_id: int,
        session: AsyncSession,
    ) -> User:
        locale = "ru"

        user: User = await user_dal.create(
            tg_id=user_tg_id,
            session=session,
            locale=locale,
        )

        await session.commit()

        return user
