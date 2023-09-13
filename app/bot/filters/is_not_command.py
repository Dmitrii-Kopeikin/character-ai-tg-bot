from aiogram.types import Message
from aiogram.filters import Filter


class IsNotCommand(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: Message):
        return not message.text.startswith("/")
