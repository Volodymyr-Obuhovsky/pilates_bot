from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Banners, Users, Marathons, Descriptions


# ****************** Work with descriptions ********************

async def get_all_descriptions(session: AsyncSession):
    query = select(Descriptions)
    result = await session.execute(query)
    return result.scalars().all()


async def get_description(session: AsyncSession, description_id: int):
    query = select(Descriptions).where(Descriptions.id == description_id)
    result = await session.execute(query)
    return result.scalar()


async def add_description(session: AsyncSession, header, text):
    new_description = Descriptions(header=header, text=text)
    session.add(new_description)
    await session.commit()
    return new_description.id


async def update_description(session: AsyncSession,
                             description_id: int,
                             header: str,
                             text: str):
    query = select(Descriptions).where(Descriptions.id == description_id)
    description = await session.execute(query)
    if not description:
        return

    query_update = (update(Descriptions).
                    where(Descriptions.id == description.scalar().id).
                    values(header=header, text=text))
    await session.execute(query_update)
    await session.commit()


async def delete_description(session: AsyncSession, description_id: int):
    query = delete(Descriptions).where(Descriptions.id == description_id)
    await session.execute(query)
    await session.commit()


# ****************** Work with banners ********************

async def get_all_banners(session: AsyncSession):
    query = select(Banners)
    result = await session.execute(query)
    return result.scalars().all()


async def get_banner(session: AsyncSession, banner_name: str):
    query = select(Banners).where(Banners.name == banner_name)
    result = await session.execute(query)
    return result.scalar()


async def add_banner_description(session: AsyncSession,
                                 banner_name: str,
                                 header: str,
                                 description: str):
    query = select(Banners)
    all_banners = (await session.execute(query)).scalars().all()
    banner_names = [banner.name for banner in all_banners]
    if banner_name in banner_names:
        return

    description_id = await add_description(session, header=header, text=description)

    session.add(Banners(name=banner_name, description_id=description_id))
    await session.commit()


async def update_banner(session: AsyncSession,
                        banner_name: str,
                        header: str,
                        description: str,
                        data: dict):
    query = select(Banners).where(Banners.name == banner_name)
    banner = await session.execute(query)
    if not banner:
        return

    await update_description(session, description_id=banner.scalar().description_id,
                             header=header, text=description)

    query_update = (update(Banners).
                    where(Banners.id == banner.scalar().id).
                    values(**data))
    await session.execute(query_update)
    await session.commit()


async def change_banner_image(session: AsyncSession, banner_name: str, image: str):
    query = update(Banners).where(Banners.name == banner_name).values(image=image)
    await session.execute(query)
    await session.commit()


# ****************** Work with marathons ********************

async def get_all_marathons(session: AsyncSession):
    query = select(Marathons)
    result = await session.execute(query)
    return result.scalars().all()


async def get_marathons(session: AsyncSession, marathon_name: str):
    query = select(Marathons).where(Marathons.name == marathon_name)
    result = await session.execute(query)
    return result.scalar()


async def add_marathon(session: AsyncSession,
                       header: str,
                       text: str,
                       marathon_data: dict):
    query = select(Marathons)
    all_marathons = (await session.execute(query)).scalars().all()
    marathons_names = [marathon.name for marathon in all_marathons]
    if marathon_data["name"] in marathons_names:
        return

    description_id = await add_description(session, header=header, text=text)
    marathon_data["description_id"] = description_id

    session.add(Marathons(**marathon_data))
    await session.commit()


async def update_marathon(session: AsyncSession,
                          marathon_name: str,
                          header: str,
                          description: str,
                          data: dict):
    query = select(Marathons).where(Marathons.name == marathon_name)
    marathon = await session.execute(query)
    if not marathon:
        return

    await update_description(session, description_id=marathon.scalar().description_id,
                             header=header, text=description)

    query_update = (update(Marathons).
                    where(Banners.id == marathon.scalar().id).
                    values(**data))
    await session.execute(query_update)
    await session.commit()



