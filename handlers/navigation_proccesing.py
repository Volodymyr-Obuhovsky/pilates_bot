from aiogram.types import InputMediaPhoto
from sqlalchemy.ext.asyncio import AsyncSession

from database.crud import BannerQuery, MarathonsQuery, ReviewQuery
from keyboards.inline import (main_page_buttons,
                              info_pages_buttons,
                              marathons_buttons,
                              marathon_button, admin_panel_buttons, change_marathon_buttons, buy_buttons,
                              change_review_buttons, review_buttons, review_button)
from utils.paginator import Paginator


async def main_page(level: int, full_user_name: str, role: str, banner_name: str):
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")

    banner_description = f"<strong>{full_user_name}{banner.description.header}</strong>🧘‍♂️\n{banner.description.text}"
    image = InputMediaPhoto(media=banner.image, caption=banner_description)

    keyboard = await main_page_buttons(level, role, full_user_name)

    return image, keyboard


# ********************* Functions for user menu **************************


async def info_pages(level: int, full_user_name: str,
                     banner_name: str, role: str):
    # Info_pages:marathons, payment_page, about_page, reviews_page
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")
    header = f"<strong>{banner.description.header}</strong>"
    if banner_name == "about":
        header = f"<strong>{banner.description.header}{full_user_name}</strong>"
    banner_description = f"{header}\n{banner.description.text}"
    image = InputMediaPhoto(media=banner.image, caption=banner_description)

    if banner_name == "marathons":
        keyboard = await marathons_buttons(level=level, role=role, full_user_name=full_user_name)
    elif banner_name == "reviews":
        keyboard = await review_buttons(level=level, role=role, full_user_name=full_user_name)
    else:
        keyboard = await info_pages_buttons(level=level, role=role,
                                            full_user_name=full_user_name)

    return image, keyboard


def pages(paginator: Paginator):
    buttons = dict()
    if paginator.has_previous():
        buttons["◀ Пред."] = "previous"

    if paginator.has_next():
        buttons["След. ▶"] = "next"

    return buttons


async def review_page(level: int, page: int, full_user_name: str, role: str):
    all_reviews = await ReviewQuery.get_all_instances(relationship="description")

    paginator = Paginator(all_reviews, page=page)
    review = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=review.image,
        caption=f"<strong>{review.description.header}</strong>"
    )

    pagination_buttons = pages(paginator)

    keyboard = await review_button(
        level=level,
        page=page,
        pagination_buttons=pagination_buttons,
        full_user_name=full_user_name,
        role=role
    )

    return image, keyboard


async def marathon_page(level: int, page: int, full_user_name: str, role: str):
    all_marathons = await MarathonsQuery.get_all_instances(relationship="description")

    paginator = Paginator(all_marathons, page=page)
    marathon = paginator.get_page()[0]

    image = InputMediaPhoto(
        media=marathon.image,
        caption=f"<strong>{marathon.description.header}\
                </strong>\n{marathon.description.text}\nСтоимость: {round(marathon.price, 2)} евро"
        # <strong>Марафон {paginator.page} из {paginator.pages}</strong>",
    )

    pagination_buttons = pages(paginator)

    keyboard = await marathon_button(
        level=level,
        page=page,
        pagination_buttons=pagination_buttons,
        full_user_name=full_user_name,
        role=role
    )

    return image, keyboard


async def buy_marathon(level: int, banner_name: str, full_user_name: str, role: str):
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")
    header = f"<strong>{banner.description.header}</strong>"
    image = InputMediaPhoto(media=banner.image, caption=header)

    keyboard = await buy_buttons(level=level, banner_name=banner_name,
                                 full_user_name=full_user_name, role=role)

    return image, keyboard


# ********************** Functions for admin_panel ******************


async def admin_panel(banner_name: str, full_user_name: str, after_add: bool):
    banner = await BannerQuery.get_instance(instance_name=banner_name, relationship="description")
    banner_description = f"<strong>{banner.description.header}</strong>\n{banner.description.text}"
    image = InputMediaPhoto(media=banner.image, caption=banner_description)

    keyboard = await admin_panel_buttons(full_user_name)

    return image, keyboard


async def get_marathon_capacities(marathon: str, full_user_name: str):
    marathon_data = await MarathonsQuery.get_instance(instance_name=marathon, relationship="description")
    header = f"<strong>{marathon_data.description.header}</strong>"
    image = InputMediaPhoto(media=marathon_data.image, caption=header)
    keyboard = await change_marathon_buttons(marathon_id=marathon_data.id,
                                             marathon=marathon_data.name,
                                             full_user_name=full_user_name)

    return image, keyboard


async def get_review_capacities(review: str, full_user_name: str):
    review_data = await ReviewQuery.get_instance(instance_name=review, relationship="description")
    header = f"<strong>{review_data.description.header}</strong>"
    image = InputMediaPhoto(media=review_data.image, caption=header)
    keyboard = await change_review_buttons(review=review,
                                           review_id=review_data.id,
                                           full_user_name=full_user_name)

    return image, keyboard


async def get_banner_data(level: int,
                          full_user_name: str | None = None,
                          banner_name: str | None = None,
                          review: str | None = None,
                          page: int | None = None,
                          role: str = "user",
                          after_add: bool = False):
    if banner_name == "admin_panel":
        return await admin_panel(banner_name=banner_name, full_user_name=full_user_name, after_add=after_add)
    if review:
        return await review_page(level=level, page=page, full_user_name=full_user_name, role=role)
    if not level:
        return await main_page(level=level, full_user_name=full_user_name, role=role, banner_name=banner_name)
    if level == 1:
        return await info_pages(level=level, full_user_name=full_user_name, banner_name=banner_name, role=role)
    if level == 2:
        return await marathon_page(level=level, page=page, full_user_name=full_user_name, role=role)
    if level == 3:
        return await buy_marathon(level=level, banner_name=banner_name, full_user_name=full_user_name, role=role)
