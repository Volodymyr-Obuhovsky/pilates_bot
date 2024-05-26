import os
from typing import Dict, Any

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, or_f

from app_filters.chat_types import ChatTypes
from app_filters.callback_query import MenuCallbackFilter
from handlers.navigation_proccesing import get_banner_data, get_marathon_capacities
from keyboards.inline import MenuCallBack
from keyboards.reply import get_keyboard

user_private_router = Router()
user_private_router.message.filter(ChatTypes(["private"]))


@user_private_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    user = message.from_user.username
    full_user_name = message.from_user.full_name
    admin = os.getenv("ADMIN")

    role = "user"
    if user == admin:
        role = "admin"

    media, keyboards = await get_banner_data(level=0, full_user_name=full_user_name, banner_name="main", role=role)
    await message.answer_photo(media.media, caption=media.caption, reply_markup=keyboards)


@user_private_router.callback_query(MenuCallbackFilter())
async def user_menu(callback: CallbackQuery, callback_data: Dict[str, Any]):
    media, keyboards = await get_banner_data(level=callback_data["level"],
                                             full_user_name=callback_data["full_user_name"],
                                             banner_name=callback_data["banner_name"],
                                             page=callback_data["page"],
                                             role=callback_data["role"],
                                             after_add=callback_data["after_add"])
    if callback_data["after_add"]:
        await callback.message.answer_photo(media.media, caption=media.caption, reply_markup=keyboards)
    else:
        await callback.message.edit_media(media=media, reply_markup=keyboards)
        await callback.answer()
