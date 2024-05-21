from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import BannerQuery, MarathonsQuery
from keyboards.inline import (main_page_buttons,
                              info_pages_buttons,
                              marathons_buttons,
                              marathon_button, admin_panel_buttons, change_marathon_buttons)
from utils.paginator import Paginator


async def main_page(level: int, role: str, banner_name: str):
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")

    banner_description = banner.description.header + "\n" + banner.description.text
    image = InputMediaPhoto(media=banner.image, caption=banner_description)

    keyboard = main_page_buttons(level, role)

    return image, keyboard


# ********************* Functions for user menu **************************


async def info_pages(level: int, banner_name: str, role: str):
    # Info_pages:marathons, payment_page, about_page, faq_page
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")
    banner_description = banner.description.header + "\n" + banner.description.text
    image = InputMediaPhoto(media=banner.image, caption=banner_description)

    if banner_name == "marathons":
        keyboard = await marathons_buttons(level=level, role=role)
    else:
        keyboard = info_pages_buttons(level=level, role=role)

    return image, keyboard


def pages(paginator: Paginator):
    buttons = dict()
    if paginator.has_previous():
        buttons["◀ Пред."] = "previous"

    if paginator.has_next():
        buttons["След. ▶"] = "next"

    return buttons


async def marathon_page(level: int, page: int):
    all_marathons = await MarathonsQuery.get_all_instances(relationship="description")

    paginator = Paginator(all_marathons, page=page)
    marathon = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=marathon.image,
        caption=f"<strong>{marathon.description.header}\
                </strong>\n{marathon.description.text}\nСтоимость: {round(marathon.price, 2)}\n\
                <strong>Товар {paginator.page} из {paginator.pages}</strong>",
    )

    pagination_buttons = pages(paginator)

    keyboard = marathon_button(
        level=level,
        page=page,
        pagination_buttons=pagination_buttons
    )

    return image, keyboard


async def inquirer():
    pass


# ********************** Functions for admin_panel ******************


async def admin_panel(banner_name: str, after_add: bool):
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")
    banner_description = banner.description.header + "\n" + banner.description.text
    image = InputMediaPhoto(media=banner.image, caption=banner_description)

    keyboard = admin_panel_buttons()

    return image, keyboard


async def get_marathon_capacities(marathon: str):
    marathon_data = await MarathonsQuery.get_instance(instance_name=marathon, relationship="description")
    header = marathon_data.description.header
    image = InputMediaPhoto(media=marathon_data.image, caption=header)
    keyboard = change_marathon_buttons(marathon_id=marathon_data.id,
                                       marathon=marathon_data.name)

    return image, keyboard


async def get_banner_data(level: int,
                          banner_name: str | None = None,
                          page: int | None = None,
                          role: str = "user",
                          after_add: bool = False):
    if banner_name == "admin_panel":
        return await admin_panel(banner_name=banner_name, after_add=after_add)
    if not level:
        return await main_page(level=level, role=role, banner_name=banner_name)
    if level == 1:
        return await info_pages(level=level, banner_name=banner_name, role=role)
    if level == 2:
        return await marathon_page(level=level, page=page)

