from aiogram.filters import Filter
from aiogram import types, Bot


# chat_types: private, group, supergroup, channel
class ChatTypes(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, messages: types.Message, bot: Bot) -> bool:
        return messages.from_user.id in bot.admin_list
