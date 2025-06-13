import os

from sqlalchemy import create_engine, MetaData, Table


def get_db_url():
    url_args = (os.getenv("DB_USER"), os.getenv("DB_PASSWORD"),
                os.getenv("DB_HOST"),os.getenv("DB_PORT"),
                os.getenv("DB_NAME"),)
    return "postgresql://{}:{}@{}:{}/{}".format(*url_args)


engine = create_engine(get_db_url())
metadata = MetaData()

user_table = Table(
    "users_customuser",
    metadata,
    autoload_with=engine
)
