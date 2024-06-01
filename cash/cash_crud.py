import json
import re
from datetime import datetime

from cash.cash_config import redis

menu_callback_attrs = {"full_user_name": None, "level": None, "banner_name": None,
                       "marathon": None, "page": 1, "role": "user", "after_add": False}

admin_callback_attrs = {"banner": None, "full_user_name": None, "marathon": None,
                        "marathon_id": None, "capacity": None, "attribute": None,
                        "change": False, "delete": False, "after_add": False}


def create_callback_data(data: dict, panel: str = "standard_menu"):
    callback_attributes = {}

    attributes = menu_callback_attrs
    if panel == "admin":
        attributes = admin_callback_attrs

    for attr in attributes:
        if data.get(attr) is not None:
            callback_attributes[attr] = data[attr]
        else:
            callback_attributes[attr] = attributes[attr]

    return callback_attributes


async def save_callback_data(data: dict, panel: str) -> str:
    callback_data = create_callback_data(data, panel)
    key = f"{datetime.utcnow().isoformat().replace(':', '-')}"
    async with await redis.get_connection() as connection:
        value = json.dumps(callback_data)
        await connection.set(key, value, ex=3600)  # Данные будут храниться 1 час
    return key


async def get_callback_data(key: str) -> dict | None:
    pattern = r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.\d+'
    key = re.search(pattern=pattern, string=key).group()
    async with await redis.get_connection() as connection:
        value = await connection.get(key)
        if value:
            data = json.loads(value)
            return data
        return None
