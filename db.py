# from sqlalchemy import create_engine


# DATABASE_URL = (
#     "postgresql+psycopg://external:external@127.0.0.1:5432/external"
# )


# engine = create_engine(
#     DATABASE_URL,
#     pool_size=10,
#     max_overflow=20
# )

import psycopg
from config import DB_CONFIG


def get_connection():

    return psycopg.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )