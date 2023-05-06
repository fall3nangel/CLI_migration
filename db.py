import os

from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    metadata = MetaData(schema='public',
                        naming_convention={
                        "ix": "ix_%(column_0_label)s",
                        "uq": "uq_%(table_name)s_%(column_0_name)s",
                        "ck": "ck_%(table_name)s_%(constraint_name)s",
                        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                        "pk": "pk_%(table_name)s",
    })


load_dotenv()

engine = create_async_engine(os.environ['DATABASE_URL_ORM'])
Session = async_sessionmaker(engine, expire_on_commit=False)
