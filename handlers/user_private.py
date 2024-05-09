from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f
from aiogram.utils.markdown import hbold
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from app_filters.chat_types import ChatTypes
from keyboards.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypes(["private"]))

GENERAL_KEYBOARD = get_keyboard(buttons=("Марафоны", "Варианты оплаты", "FAQ", "Контакты"),
                                placeholder="Что Вас интересует?",
                                size=(2, 2))
MARATHON_KEYBOARD = get_keyboard(buttons=("СПИНА- РУКИ", "ПОПА - НОГИ", "ПРЕСС - СПИНА", "ПРЕСС - ТАЗ"),
                                 size=(2, 2))


@user_private_router.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}, это PilatesMari_Bot - помощник тренера Марии по пилатесу",
        reply_markup=GENERAL_KEYBOARD)


@user_private_router.message(or_f(F.text.lower() == "марафоны", Command("maraphons")))
async def marathons_cmd(message: Message) -> None:
    await message.answer(f"Выберите, что бы Вы хотели укрепить💪",
                         reply_markup=MARATHON_KEYBOARD)


@user_private_router.message(F.text.lower() == "варианты оплаты")
async def payment_options(message: Message) -> None:
    response = as_marked_section(
        Bold("Варианты оплаты:"),
        "Monobank",
        "Bunq",
        marker="✅"
    )
    await message.answer(text=response.as_html())
# F - is magic filter
# @user_private_router.message(F.text)
# async def test(message: Message) -> None:
#     await message.answer("This is magic filter")
