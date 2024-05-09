from aiogram import types, Router, Bot
from aiogram.filters import Command

from app_filters.chat_types import ChatTypes, IsAdmin
from keyboards.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypes(['private']), IsAdmin())
admin_router.edited_message.filter(ChatTypes(['private']), IsAdmin())

ADMIN_KEYBOARD = get_keyboard(buttons=("Добавить курс", "Добавить фото", "Скрыть кнопки"),
                              size=(1, 1, 1),
                              placeholder="Выберите действие")


@admin_router.message(Command("admin"))
async def admin_handler(message: types.Message) -> None:
    await message.answer("", reply_markup=ADMIN_KEYBOARD)
