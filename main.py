import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram.fsm.strategy import FSMStrategy

from environment import set_environment

set_environment("dev_local")

from cash.cash_config import redis
from common.texts_for_db import fill_db
from database.db_config import create_db, drop_db
from handlers.admin_private import admin_router
from handlers.user_private import user_private_router
from middleware.cash import CallbackMiddleware

# receive our token from environment variables
TOKEN_API = os.environ.get("BOT_TOKEN")

bot = Bot(TOKEN_API, parse_mode=ParseMode.HTML)
bot.admin_list = []

# fsmstrategy - keeps every chat state with every user(USER_IN_CHAT state by default)
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)

# @dp.message(F.photo)
# async def photo(message: types.Message):
#     await message.answer(text=message.photo[-1].file_id)

dp.callback_query.outer_middleware(CallbackMiddleware())

dp.include_routers(user_private_router, admin_router)


async def on_startup():
    await redis.init_cash()


async def on_shutdown():
    await redis.close_cash()


async def main() -> None:
    await drop_db()
    await create_db()
    await fill_db()

    # it is necessary for situation, when bot hasn't worked anytime and
    # after start, it will not answer on collected messages in chat
    await bot.delete_webhook(drop_pending_updates=True)

    # delete bot menu
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())

    # only updates is pointed in allowed_updates will be handled
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(),
                           on_startup=on_startup, on_shutdown=on_shutdown)

    # await drop_db()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
