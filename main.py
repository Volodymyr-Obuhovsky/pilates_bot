import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats, Message
from aiogram.fsm.strategy import FSMStrategy

from environment import set_environment

set_environment("test_local")

from common.commands import private_commands
from database.db_config import create_db, drop_db
from handlers.admin_private import admin_router
from handlers.info import info_router
from handlers.user_private import user_private_router
from handlers.faq import faq_router

# receive our token from environment variables
TOKEN_API = os.environ.get("BOT_TOKEN")

# fsmstrategy - keeps every chat state with every user(USER_IN_CHAT state by default)
dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_CHAT)
# ALLOWED_UPDATES = ["message", "edited_message"]

bot = Bot(TOKEN_API, parse_mode=ParseMode.HTML)
bot.admin_list = []


dp.include_routers(user_private_router, admin_router)


async def main() -> None:
    await create_db()

    # it is necessary for situation, when bot hasn't worked anytime and
    # after start, it will not answer on collected messages in chat
    await bot.delete_webhook(drop_pending_updates=True)

    # create bot menu
    await bot.set_my_commands(commands=private_commands, scope=BotCommandScopeAllPrivateChats())

    # delete bot menu
    await bot.delete_my_commands(scope=BotCommandScopeAllPrivateChats())

    # only updates is pointed in allowed_updates will be handled
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    # await drop_db()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
