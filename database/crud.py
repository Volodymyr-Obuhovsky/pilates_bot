from sqlalchemy import select, update

from db_config import db_context, inspector
from models import Descriptions, Banners, Marathons, Users


class AsyncCrud:
    DB_TABLE = None
    HAS_SUB_INSTANCE: bool = False
    SUB_INSTANCE = None

    @classmethod
    async def get_column_names(cls):
        columns = inspector.get_columns(cls.DB_TABLE.__tablename__)
        return [column["name"] for column in columns if column["name"] != "id"]

    @classmethod
    async def get_all_instances(cls):
        async with db_context() as session:
            query = select(cls.DB_TABLE)
            result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_instance(cls, instance_id: int = None, instance_name: str = None):
        # We can get our instance by id or by name
        async with db_context() as session:
            if instance_id:
                query = select(cls.DB_TABLE).where(cls.DB_TABLE.id == instance_id)
            else:
                query = select(cls.DB_TABLE).where(cls.DB_TABLE.name == instance_name)
            result = await session.execute(query)
        return result.scalar()

    @classmethod
    async def add_instance(cls, new_instance: dict):
        async with db_context() as session:
            if not cls.HAS_SUB_INSTANCE:
                session.add(cls.DB_TABLE(**new_instance))
                await session.commit()
                return cls.DB_TABLE.id

            query = select(cls.DB_TABLE)
            all_instances = (await session.execute(query)).scalars().all()
            instance_names = [instance.name for instance in all_instances]
            if new_instance["name"] in instance_names:
                return

            sub_instance = await cls.add_instance(cls.SUB_INSTANCE())
            new_instance[cls.SUB_INSTANCE.__tablename__ + "_id"] = sub_instance

            session.add(cls.DB_TABLE(**new_instance))
            await session.commit()

    @classmethod
    async def update_instance(cls, new_instance_data: dict,
                              instance_id: int,
                              instance_name: str):
        async with db_context() as session:
            if instance_id:
                instance = await session.execute(select(cls.DB_TABLE).filter(cls.DB_TABLE.id == instance_id))
            else:
                instance = await session.execute(select(cls.DB_TABLE).filter(cls.DB_TABLE.name == instance_name))
            if not instance:
                return

            if instance_id:
                query_update = (update(cls.DB_TABLE).
                                where(cls.DB_TABLE.id == instance_id).
                                values(**new_instance_data))
            else:
                query_update = (update(cls.DB_TABLE).
                                where(cls.DB_TABLE.name == instance_name).
                                values(**new_instance_data))
            await session.execute(query_update)
            await session.commit()

    @classmethod
    async def delete_instance(cls, instance_id: int):
        async with db_context() as session:
            instance = await session.execute(select(cls.DB_TABLE).filter(cls.DB_TABLE.id == instance_id))
            db_instance = instance.scalar_one_or_none()
            if db_instance:
                session.delete(db_instance)
                await session.commit()


class BannerQuery(AsyncCrud):
    DB_TABLE = Banners
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = Descriptions


class DescriptionsQuery(AsyncCrud):
    DB_TABLE = Descriptions
    HAS_SUB_INSTANCE = False


class MarathonsQuery(AsyncCrud):
    DB_TABLE = Marathons
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = Descriptions


class UsersQuery(AsyncCrud):
    DB_TABLE = Users
    HAS_SUB_INSTANCE = True
    SUB_INSTANCE = Marathons
