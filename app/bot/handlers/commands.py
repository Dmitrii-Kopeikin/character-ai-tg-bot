from aiogram.types import Message

from config import config

from ..keyboards import get_choose_character_keyboard


async def start_handler(
    message: Message,
) -> None:
    await message.answer(
        text="Привет. Я могу разговаривать от лица различных персонажей.\n",
    )
    await menu_handler(message)


async def menu_handler(
    message: Message,
) -> None:
    await message.answer(
        text="Выбери персонажа:",
        reply_markup=get_choose_character_keyboard(
            f"{config.server.host}/choose_character"
            f"?user_tg_id={message.from_user.id}",
        ),
    )
