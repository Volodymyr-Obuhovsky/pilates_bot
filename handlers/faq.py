from aiogram import types, Router, F
from aiogram.filters import Command, or_f

from keyboards.reply import del_keyboard

faq_router = Router()


@faq_router.message(or_f((F.text.lower() == "faq"), Command("faq")))
async def faq_command(message: types.Message) -> None:
    await message.answer("Here will be part chapter with FAQ", reply_markup=del_keyboard)
