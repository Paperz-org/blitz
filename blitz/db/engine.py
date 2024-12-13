from functools import lru_cache
from typing import Any

from sqlalchemy import Engine, pool
from sqlmodel import create_engine as _create_engine


@lru_cache
def create_engine(url: str, **kwargs: dict[str, Any]) -> Engine:
    return _create_engine(url, connect_args={**kwargs}, poolclass=pool.StaticPool)
