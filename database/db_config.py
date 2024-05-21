import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import inspect

from database.models import Base

# from database.orm_query import orm_add_banner_description, orm_create_categories

# from common.texts_for_db import categories, description_for_info_pages
from environment import set_environment

set_environment("test_local")

engine = create_async_engine(os.getenv('DB_URL'), echo=True, pool_pre_ping=True,
                             pool_recycle=1800)

db_context = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# async def get_db():
#     try:
#         yield SessionLocal()
#     finally:
#         await SessionLocal().close()

#
# def db_context():
#     async with SessionLocal() as session:
#         yield session


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
