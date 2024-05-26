import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from cash.cash_crud import get_callback_data


class CallbackMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.callback_data = None

    @staticmethod
    async def __on_pre_process_callback_query(key):
        try:
            callback_data = await get_callback_data(key)
            if not callback_data:
                return
            return callback_data
        except Exception as e:
            logging.info(f"Error retrieving callback data: {e}")
            raise Exception()

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        if not event.data:
            return await handler(event, data)
        self.callback_data = await self.__on_pre_process_callback_query(event.data)
        data['callback_data'] = self.callback_data
        return await handler(event, data)
