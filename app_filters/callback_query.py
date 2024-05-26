from aiogram.filters import Filter
from aiogram import types


class MenuCallbackFilter(Filter):

    def __init__(self):
        pass

    async def __call__(self, callback_query: types.CallbackQuery,
                       callback_data):
        if callback_query.data.startswith("main"):
            return True
        return False


class AdminCallbackFilter(Filter):

    def __init__(self, *true_attrs, **conditions):
        self.true_attrs = true_attrs
        self.conditions = conditions

    async def __call__(self, callback_query: types.CallbackQuery,
                       callback_data):

        for key, value in self.conditions.items():
            if callback_data.get(key) != value:
                return False
        if self.true_attrs:
            return all(False for attr in self.true_attrs if not callback_data[attr])
        return True

