from functools import lru_cache

from sqlalchemy import Engine

from blitz.db.engine import create_engine


@lru_cache()
def get_in_memory_engine() -> Engine:
    url = "sqlite:///"
    return create_engine(url, check_same_thread=False)
