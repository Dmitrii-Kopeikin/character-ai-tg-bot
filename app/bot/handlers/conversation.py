from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.amplitude_client import amplitude_client
from app.database.dal import conversation_request_dal, user_dal
from app.open_ai import OpenAiException, open_ai


async def message_handler(
    message: Message,
    user_id: int,
    session: AsyncSession,
) -> None:
    await message.bot.send_chat_action(message.from_user.id, "typing")

    user = await user_dal.get(id=user_id, session=session, prefetch=True)
    character = await user.current_conversation.awaitable_attrs.character

    request_text = message.text

    conversation_request = await conversation_request_dal.create(
        conversation_id=user.current_conversation_id,
        request_message=request_text,
        session=session,
    )

    await session.commit()

    amplitude_client.track_request(
        user_id=user.id,
        data={
            "conversation_id": user.current_conversation_id,
            "conversation_request_id": conversation_request.id,
        },
    )

    try:
        result = await open_ai.request_by_gateway(
            system_message=character.prompt,
            user_message=request_text,
        )
    except OpenAiException:
        await message.answer(
            text="Произошла ошибка. Пожалуйста попробуйте еще раз."
        )
        return

    amplitude_client.track_response(
        user_id=user.id,
        data={
            "conversation_id": user.current_conversation_id,
            "conversation_request_id": conversation_request.id,
        },
    )

    response_text = result["choices"][0]["message"]["content"]

    await conversation_request_dal.update_response(
        id=conversation_request.id,
        response_message=response_text,
    )

    await session.commit()

    await message.answer(
        text=response_text,
    )

    amplitude_client.track_response_sent_to_user(
        user_id=user.id,
        data={
            "conversation_id": user.current_conversation_id,
            "conversation_request_id": conversation_request.id,
        },
    )
