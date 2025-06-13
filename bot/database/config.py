import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Column, Integer, String, MetaData, Table


def get_db_url():
    url_args = (os.getenv("DB_USER"), os.getenv("DB_PASSWORD"),
                os.getenv("DB_HOST"),os.getenv("DB_PORT"),
                os.getenv("DB_NAME"),)
    return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(*url_args)


engine = create_async_engine(get_db_url())
metadata = MetaData()

user_table = Table(
    "users_customuser",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("phone", String),
    Column("telegram_chat_id", Integer)
)
