import os

from redis.asyncio import from_url

CASH_URL = os.getenv("CASH")


class Cash:

    def __init__(self):
        self._redis = None

    async def init_cash(self):
        self._redis = from_url(url=CASH_URL,
                               encoding="utf_8",
                               decode_responses=True)
        return self._redis

    async def close_cash(self):
        self._redis.close()

    async def get_connection(self):
        return await self.init_cash()


redis = Cash()
