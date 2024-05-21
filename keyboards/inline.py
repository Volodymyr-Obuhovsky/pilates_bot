from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.crud import MarathonsQuery


class MenuCallBack(CallbackData, prefix="main"):
    level: int
    banner_name: str | None = None
    marathon: str | None = None
    page: int = 1
    role: str = "user"
    after_add: bool = False


class AdminCallBack(CallbackData, prefix="admin"):
    banner: str | None = None
    marathon: str | None = None
    marathon_id: int | None = None
    capacity: str | None = None
    attribute: str | None = None
    change: bool = False
    after_add: bool = False


def main_page_buttons(level: int, role: str,
                      sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    buttons = {
        "МАРАФОНЫ 🏃‍♀️": "marathons",
        "ОПЛАТА💵": "payment",
        "О НАС ℹ️": "about",
        "FAQ 📃": "faq"
    }
    for button, banner in buttons.items():
        keyboard.add(InlineKeyboardButton(text=button,
                                          callback_data=MenuCallBack(level=level + 1,
                                                                     banner_name=banner,
                                                                     role=role).pack()))
    if role == "admin":
        keyboard.add(InlineKeyboardButton(text="АДМИН-ПАНЕЛЬ⚙️",
                                          callback_data=AdminCallBack(banner="admin_panel").pack()))

    return keyboard.adjust(*sizes).as_markup()


def admin_panel_buttons(sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="ДОБАВИТЬ МАРАФОН",
                                      callback_data=AdminCallBack(banner="add_marathon").pack()))
    keyboard.add(InlineKeyboardButton(text="ИЗМЕНИТЬ МАРАФОН",
                                      callback_data=AdminCallBack(banner="change_marathon").pack()))
    keyboard.add(InlineKeyboardButton(text="⬅️НАЗАД",
                                      callback_data=MenuCallBack(level=0, banner_name="main", role="admin").pack()))
    keyboard.add(InlineKeyboardButton(text="НА ГЛАВНУЮ🏠",
                                      callback_data=MenuCallBack(level=0, banner_name="main", role="admin").pack()))
    return keyboard.adjust(*sizes).as_markup()


def info_pages_buttons(level: int, role: str, sizes: tuple[int] = (2,)):
    # Info_pages: payment_page, about_page, faq_page
    keyboard = InlineKeyboardBuilder()

    buttons = {
        "⬅️НАЗАД": "main",
        "МАРАФОНЫ🏃‍♀️": "marathons",
        "НА ГЛАВНУЮ🏠": "main",
    }
    for button, banner in buttons.items():

        if banner == "marathons":
            keyboard.add(InlineKeyboardButton(text=button,
                                              callback_data=MenuCallBack(level=level, banner_name=banner,
                                                                         role=role).pack()))
            continue
        keyboard.add(InlineKeyboardButton(text=button,
                                          callback_data=MenuCallBack(level=level - 1, banner_name=banner,
                                                                     role=role).pack()))

    return keyboard.adjust(*sizes).as_markup()


async def marathons_buttons(level: int,
                            role: str,
                            sizes: tuple[int] = (2,),
                            change_button: bool = False):
    keyboard = InlineKeyboardBuilder()
    marathons = await MarathonsQuery.get_all_instances(relationship="description")
    buttons = {marathon.description.header: marathon.name for marathon in marathons}

    for button, banner in buttons.items():
        if not change_button:
            keyboard.add(InlineKeyboardButton(text=button,
                                              callback_data=MenuCallBack(level=level + 1, banner_name=banner,
                                                                         role=role).pack()))
        else:
            keyboard.add(InlineKeyboardButton(text=button,
                                              callback_data=AdminCallBack(marathon=banner,
                                                                          change=True).pack()))
    if not change_button:
        keyboard.add(InlineKeyboardButton(text="⬅️НАЗАД",
                                          callback_data=MenuCallBack(level=0, banner_name="main", role=role).pack()))
    else:
        keyboard.add(InlineKeyboardButton(text="⬅️НАЗАД",
                                          callback_data=AdminCallBack(banner="admin_panel",
                                                                      after_add=True).pack()))

    return keyboard.adjust(*sizes).as_markup()


def marathon_button(level: int, page: int,
                    pagination_buttons: dict,
                    sizes: tuple[int] = (2, 1)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="⬅️НАЗАД",
                                      callback_data=MenuCallBack(level=level - 1, banner_name="marathons").pack()))
    keyboard.add(InlineKeyboardButton(text="КУПИТЬ💶",
                                      callback_data=MenuCallBack(level=level + 3, banner_name="buy").pack()))
    keyboard.add(InlineKeyboardButton(text="НА ГЛАВНУЮ🏠",
                                      callback_data=MenuCallBack(level=0, banner_name="main").pack()))
    keyboard.adjust(*sizes)
    row = []
    for text, banner in pagination_buttons.items():
        if banner == "next":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                banner_name=banner,
                                                page=page + 1).pack()))

        elif banner == "previous":
            row.append(InlineKeyboardButton(text=text,
                                            callback_data=MenuCallBack(
                                                level=level,
                                                banner_name=banner,
                                                page=page - 1).pack()))

    return keyboard.row(*row).as_markup()


def change_marathon_buttons(marathon_id: int,
                            marathon: str,
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
        keyboard.add(InlineKeyboardButton(text=capacity,
                                          callback_data=AdminCallBack(marathon_id=marathon_id,
                                                                      marathon=marathon,
                                                                      capacity=capacity,
                                                                      attribute=attribute).pack()))
    #
    keyboard.add(InlineKeyboardButton(text="⬅️НАЗАД",
                                      callback_data=AdminCallBack(banner="change_marathon").pack()))
    return keyboard.adjust(*sizes).as_markup()


def finish_add_marathon_buttons(sizes: tuple[int] = (1,)):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="НА ГЛАВНУЮ🏠",
                                      callback_data=MenuCallBack(level=0,
                                                                 banner_name="main",
                                                                 role="admin",
                                                                 after_add=True).pack()))
    keyboard.add(InlineKeyboardButton(text="АДМИН-ПАНЕЛЬ⚙️",
                                      callback_data=AdminCallBack(banner="admin_panel", after_add=True).pack()))
    return keyboard.adjust(*sizes).as_markup()


def get_callback_buttons(buttons: dict[str, str], sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for text, data in buttons.items():
        keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

    return keyboard.adjust(*sizes).as_markup()
