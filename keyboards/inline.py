from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from cash.cash_crud import save_callback_data, get_callback_data
from database.crud import MarathonsQuery


class MenuCallBack(CallbackData, prefix="main"):
    data_key: str


class AdminCallBack(CallbackData, prefix="admin"):
    data_key: str


async def create_button(button: str, callback_data: dict, panel: str):
    key = await save_callback_data(data=callback_data,
                                   panel=panel)
    if panel == "admin":
        return InlineKeyboardButton(text=button,
                                    callback_data=AdminCallBack(data_key=key).pack())
    return InlineKeyboardButton(text=button,
                                callback_data=MenuCallBack(data_key=key).pack())


async def main_page_buttons(level: int, role: str,
                            full_user_name: str,
                            sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    buttons = {
        "МАРАФОНЫ 🏃‍♀️": "marathons",
        "ОПЛАТА💵": "payment",
        "О НАС ℹ️": "about",
        "FAQ 📃": "faq"
    }

    for button_name, banner in buttons.items():
        button = await create_button(button=button_name,
                                     callback_data=dict(level=level + 1,
                                                        full_user_name=full_user_name,
                                                        banner_name=banner,
                                                        role=role),
                                     panel="standard_panel")
        keyboard.add(button)
    if role == "admin":
        button = await create_button(button="АДМИН-ПАНЕЛЬ⚙️",
                                     callback_data=dict(banner="admin_panel",
                                                        full_user_name=full_user_name),
                                     panel="admin")
        keyboard.add(button)

    return keyboard.adjust(*sizes).as_markup()


async def admin_panel_buttons(full_user_name: str, sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    button = await create_button(button="ДОБАВИТЬ МАРАФОН",
                                 callback_data=dict(banner="add_marathon",
                                                    full_user_name=full_user_name),
                                 panel="admin")
    keyboard.add(button)
    button = await create_button(button="ИЗМЕНИТЬ МАРАФОН",
                                 callback_data=dict(banner="change_marathon",
                                                    full_user_name=full_user_name),
                                 panel="admin")
    keyboard.add(button)
    button = await create_button(button="⬅️НАЗАД",
                                 callback_data=dict(level=0, full_user_name=full_user_name,
                                                    banner_name="main", role="admin"),
                                 panel="standard_menu")
    keyboard.add(button)
    button = await create_button(button="НА ГЛАВНУЮ🏠",
                                 callback_data=dict(level=0, full_user_name=full_user_name,
                                                    banner_name="main", role="admin"),
                                 panel="standard_menu")
    keyboard.add(button)
    return keyboard.adjust(*sizes).as_markup()


async def info_pages_buttons(level: int, role: str, full_user_name: str, sizes: tuple[int] = (2,)):
    # Info_pages: payment_page, about_page, faq_page
    keyboard = InlineKeyboardBuilder()

    buttons = {
        "⬅️НАЗАД": "main",
        "МАРАФОНЫ🏃‍♀️": "marathons",
        "НА ГЛАВНУЮ🏠": "main",
    }
    for button_name, banner in buttons.items():

        if banner == "marathons":
            button = await create_button(button=button_name,
                                         callback_data=dict(level=level,
                                                            banner_name=banner,
                                                            full_user_name=full_user_name,
                                                            role=role),
                                         panel="standard_menu")

            keyboard.add(button)
            continue
        button = await create_button(button=button_name,
                                     callback_data=dict(level=level - 1, banner_name=banner,
                                                        full_user_name=full_user_name,
                                                        role=role),
                                     panel="standard_menu")
        keyboard.add(button)

    return keyboard.adjust(*sizes).as_markup()


async def marathons_buttons(level: int,
                            role: str,
                            full_user_name: str,
                            sizes: tuple[int] = (2,),
                            change_button: bool = False):
    keyboard = InlineKeyboardBuilder()
    marathons = await MarathonsQuery.get_all_instances(relationship="description")
    buttons = [(marathon.description.header,marathon.name, marathon.id) for marathon in marathons]

    for button_name, banner, page in buttons:
        if not change_button:
            button = await create_button(button=button_name,
                                         callback_data=dict(level=level + 1, banner_name=banner,
                                                            full_user_name=full_user_name,
                                                            role=role, page=page),
                                         panel="standard_menu")
            keyboard.add(button)
        else:
            button = await create_button(button=button_name,
                                         callback_data=dict(marathon=banner,
                                                            full_user_name=full_user_name,
                                                            change=True),
                                         panel="admin")

            keyboard.add(button)
    if not change_button:
        button = await create_button(button="⬅️НАЗАД",
                                     callback_data=dict(level=0, full_user_name=full_user_name,
                                                        banner_name="main", role=role),
                                     panel="standard_menu")
        keyboard.add(button)
    else:
        button = await create_button(button="⬅️НАЗАД",
                                     callback_data=dict(banner="admin_panel",
                                                        full_user_name=full_user_name,
                                                        after_add=True),
                                     panel="admin")
        keyboard.add(button)

    return keyboard.adjust(*sizes).as_markup()


async def marathon_button(level: int, page: int,
                          pagination_buttons: dict,
                          full_user_name: str, role: str,
                          sizes: tuple[int] = (2, 2, 2)):
    keyboard = InlineKeyboardBuilder()
    button = await create_button(button="⬅️НАЗАД",
                                 callback_data=dict(level=level - 1,
                                                    full_user_name=full_user_name,
                                                    banner_name="marathons",
                                                    role=role),
                                 panel="standard_menu")
    keyboard.add(button)
    button = await create_button(button="КУПИТЬ💶",
                                 callback_data=dict(level=level + 1, banner_name="buy_marathon", role=role),
                                 panel="standard_menu")

    keyboard.add(button)

    for text, banner in pagination_buttons.items():
        if banner == "next":
            button = await create_button(button=text,
                                         callback_data=dict(level=level,
                                                            banner_name=banner,
                                                            page=page + 1),
                                         panel="standard_menu")
            keyboard.add(button)

        elif banner == "previous":
            button = await create_button(button=text,
                                         callback_data=dict(level=level,
                                                            banner_name=banner,
                                                            page=page - 1),
                                         panel="standard_menu")
            keyboard.add(button)

    button = await create_button(button="НА ГЛАВНУЮ🏠",
                                 callback_data=dict(level=0, banner_name="main",
                                                    full_user_name=full_user_name, role=role),
                                 panel="standard_menu")
    keyboard.add(button)
    return keyboard.adjust(*sizes).as_markup()


async def buy_buttons(level: int, banner_name: str,
                      full_user_name: str, role: str,
                      sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    button = await create_button(button="⬅️НАЗАД",
                                 callback_data=dict(level=level - 1,
                                                    banner=banner_name,
                                                    full_user_name=full_user_name,
                                                    role=role),
                                 panel="standard_menu")
    keyboard.add(button)
    button = await create_button(button="НА ГЛАВНУЮ🏠",
                                 callback_data=dict(level=0, banner_name="main",
                                                    full_user_name=full_user_name,
                                                    role=role),
                                 panel="standard_menu")
    keyboard.add(button)

    return keyboard.adjust(*sizes).as_markup()


async def change_marathon_buttons(marathon_id: int,
                                  marathon: str,
                                  full_user_name: str,
                                  sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    buttons = {
        "НАЗВАНИЕ": "name",
        "ЗАГОЛОВОК": "header",
        "ОПИСАНИЕ": "description",
        "ЦЕНА": "price",
        "СКИДКА": "discount",
        "ИЗОБРАЖЕНИЕ": "image",

    }

    for capacity, attribute in buttons.items():
        button = await create_button(button=capacity,
                                     callback_data=dict(marathon_id=marathon_id,
                                                        marathon=marathon,
                                                        capacity=capacity,
                                                        full_user_name=full_user_name,
                                                        attribute=attribute),
                                     panel="admin")
        keyboard.add(button)
    button = await create_button(button="⬅️НАЗАД",
                                 callback_data=dict(banner="change_marathon",
                                                    full_user_name=full_user_name),
                                 panel="admin")
    keyboard.add(button)
    return keyboard.adjust(*sizes).as_markup()


async def finish_add_marathon_buttons(full_user_name: str, sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    button = await create_button(button="НА ГЛАВНУЮ🏠",
                                 callback_data=dict(level=0,
                                                    banner_name="main",
                                                    full_user_name=full_user_name,
                                                    role="admin",
                                                    after_add=True),
                                 panel="standard_menu")
    keyboard.add(button)
    button = await create_button(button="АДМИН-ПАНЕЛЬ⚙️",
                                 callback_data=dict(banner="admin_panel",
                                                    full_user_name=full_user_name,
                                                    after_add=True),
                                 panel="admin")
    keyboard.add(button)
    return keyboard.adjust(*sizes).as_markup()

# def get_callback_buttons(buttons: dict[str, str], sizes: tuple[int] = (2,)):
#     keyboard = InlineKeyboardBuilder()
#
#     for text, data in buttons.items():
#         keyboard.add(InlineKeyboardButton(text=text, callback_data=data))
#
#     return keyboard.adjust(*sizes).as_markup()
