from typing import List

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import flags

from app.amplitude_client import amplitude_client
from app.database.dal import conversation_request_dal, user_dal
from app.database.models import Character
from app.open_ai import OpenAiException, open_ai


@flags.chat_action(action="typing", initial_sleep=1.0)
async def message_handler(
    message: Message,
    user_id: int,
    session: AsyncSession,
) -> None:
    user = await user_dal.get(id=user_id, session=session, prefetch=True)
    character: Character = (
        await user.current_conversation.awaitable_attrs.character
    )
    previous_requests: List = (
        await user.current_conversation.awaitable_attrs.requests
    )

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

    context = ""

    if previous_requests:
        slice_index = len(previous_requests) - open_ai.context_requests_count
        context = "\n".join(
            [
                (
                    f"message: {request.request_message}\n"
                    f"response: {request.response_message}"
                )
                for request in previous_requests[slice_index:]
            ],
        )

    try:
        result = await open_ai.request(
            prompt=character.prompt,
            context=context,
            user_message=request_text,
            user_id=user_id,
        )
        response_text = result["choices"][0]["message"]["content"]
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

    await conversation_request_dal.update_response(
        id=conversation_request.id,
        response_message=response_text,
        session=session,
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
