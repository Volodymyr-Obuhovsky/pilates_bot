import time

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import DBAPIError

from database.db_config import db_context
from database.models import Descriptions, Banners, Marathons, Reviews, Users


class AsyncCrud:
    DB_TABLE = None
    HAS_SUB_INSTANCE: bool = False
    SUB_INSTANCE = None

    @classmethod
    async def get_all_instances(cls, relationship: str):
        async with db_context() as session:
            if relationship:
                related_attr_obj = getattr(cls.DB_TABLE, relationship)
                query = select(cls.DB_TABLE).options(joinedload(related_attr_obj))
            else:
                query = select(cls.DB_TABLE)
            result = await session.execute(query)
        all_instances = result.scalars().all()
        all_instances.sort(key=lambda x: x.id)
        return all_instances

    @classmethod
    async def get_instance(cls, instance_id: int = None,
                           instance_name: str | None = None,
                           relationship: str | None = None):
        # We can get our instance by id or by name
        async with db_context() as session:
            if relationship:
                related_attr_obj = getattr(cls.DB_TABLE, relationship)
                if instance_id:
                    query = select(cls.DB_TABLE). \
                        options(joinedload(related_attr_obj)).where(cls.DB_TABLE.id == instance_id)
                else:
                    query = select(cls.DB_TABLE). \
                        options(joinedload(related_attr_obj)).where(cls.DB_TABLE.name == instance_name)
            else:
                if instance_id:
                    query = select(cls.DB_TABLE).where(cls.DB_TABLE.id == instance_id)
                else:
                    query = select(cls.DB_TABLE).where(cls.DB_TABLE.name == instance_name)
            result = await session.execute(query)

            return result.scalar()

    @classmethod
    async def add_instance(cls, new_instance: dict, sub_data: dict = None):
        async with db_context() as session:
            try:

                if cls.HAS_SUB_INSTANCE:
                    sub_instance = cls.SUB_INSTANCE.DB_TABLE(**sub_data)
                    session.add(sub_instance)
                    await session.flush()
                    sub_instance_id = sub_instance.id
                    f_key = f"{cls.SUB_INSTANCE.DB_TABLE.__tablename__}_id"
                    new_instance.update({f_key: sub_instance_id})

                new_instance = cls.DB_TABLE(**new_instance)
                session.add(new_instance)
                await session.commit()
            except DBAPIError as e:
                await session.rollback()
                print(f"DBAPIError during database operation: {e}")
                raise
            except Exception as e:
                await session.rollback()
                print(f"Unexpected error during database operation: {e}")
                raise
            finally:
                await session.close()

    @classmethod
    async def update_instance(cls, new_instance_data: dict,
                              instance_id: int | None = None,
                              current_instance_name: str | None = None,
                              relationship: str | None = None):
        async with db_context() as session:
            # Check our instance ins db
            instance = await cls.get_instance(instance_id, current_instance_name, relationship)
            if not instance:
                return "Instance was not found"

            try:
                # Update sub_instance in relate table if exists
                if relationship and hasattr(instance, relationship):
                    sub_instance = getattr(instance, relationship)
                    sub_data = {k: v for k, v in new_instance_data.items() if hasattr(sub_instance, k)}
                    new_instance_data = {k: v for k, v in new_instance_data.items() if not hasattr(sub_instance, k)}

                    if sub_data:
                        sub_instance_id = getattr(instance, f"{relationship}_id")
                        query_update = (update(cls.SUB_INSTANCE.DB_TABLE).
                                        where(cls.SUB_INSTANCE.DB_TABLE.id == sub_instance_id).
                                        values(**sub_data))
                        await session.execute(query_update)

                # Update main instance
                if instance_id:
                    query_update = (update(cls.DB_TABLE).
                                    where(cls.DB_TABLE.id == instance_id).
                                    values(**new_instance_data))
                else:
                    query_update = (update(cls.DB_TABLE).
                                    where(cls.DB_TABLE.name == current_instance_name).
                                    values(**new_instance_data))

                await session.execute(query_update)
                await session.commit()
            except Exception as e:
                await session.rollback()
                print(f"Unexpected error during database operation: {e}")
                raise
            finally:
                await session.close()

    @classmethod
    async def delete_instance(cls, instance_id: int | None = None,
                              instance_name: str | None = None,
                              relationship: str | None = None):
        async with db_context() as session:
            try:
                instance = await cls.get_instance(instance_id, instance_name, relationship)
                if not instance:
                    return "Instance was not found"

                if relationship:
                    get_sub_instance_id = getattr(instance, f"{relationship}_id")
                    query = select(cls.SUB_INSTANCE.DB_TABLE).where(cls.SUB_INSTANCE.DB_TABLE.id == get_sub_instance_id)
                    sub_instance = (await session.execute(query)).scalar_one_or_none()
                    await session.delete(sub_instance)
                    await session.commit()

                instance = await session.merge(instance)
                await session.delete(instance)
                await session.commit()
                return "Запись была успешно удалена"
            except Exception as e:
                return f"{e}.\nЗапись не была удалена"


class DescriptionsQuery(AsyncCrud):
    DB_TABLE = Descriptions
    HAS_SUB_INSTANCE = False


class BannerQuery(AsyncCrud):
    DB_TABLE = Banners
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = DescriptionsQuery


class MarathonsQuery(AsyncCrud):
    DB_TABLE = Marathons
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = DescriptionsQuery


class UsersQuery(AsyncCrud):
    DB_TABLE = Users
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = MarathonsQuery


class ReviewQuery(AsyncCrud):
    DB_TABLE = Reviews
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = DescriptionsQuery
