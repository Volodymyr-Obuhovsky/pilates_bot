from aiogram import Router, F
from aiogram.filters import Command, or_f
from aiogram.types import Message
from aiogram.utils.markdown import hbold

info_router = Router()

LIST_COMMANDS = """
/start - начало работы с ботом
/about - о боте
/buy_maraphon - стать участником марафона
/maraphones - список доступных марафонов
/faq - часто задаваемые вопросы
/help - список комманд для взаимодействия с ботом
/contacts - контакты
"""


@info_router.message(or_f((F.text.lower() == "help"), Command("help")))
async def help_command(message: Message) -> None:
    await message.answer(LIST_COMMANDS)


@info_router.message(or_f((F.text.lower() == "about"), Command("about")))
async def about_cmd(message: Message) -> None:
    await message.answer("PilatesMari_Bot - ваш личный помощник в доступе к видеокурсам по пилатесу")


@info_router.message(or_f((F.text.lower() == "contacts"), Command("contacts")))
async def contacts_command(message: Message) -> None:
    await message.answer(f"{hbold(message.from_user.full_name)}, Вы можете связаться со мной через инстаграм, "
                         f"перейдя по ссылке https://www.instagram.com/masha.pro.pilates/")
