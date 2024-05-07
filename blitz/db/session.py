from contextlib import contextmanager
from functools import lru_cache
from typing import TYPE_CHECKING, Generator

from sqlalchemy import Engine
from sqlmodel import Session

from blitz.db.adapters.in_memory import get_in_memory_engine
from blitz.db.adapters.postgresql import get_postgresql_engine
from blitz.db.adapters.sqlite import get_sqlite_engine
from blitz.settings import DBTypes, get_settings

if TYPE_CHECKING:
    from blitz.app import BlitzApp


@contextmanager
def get_session(engine: Engine) -> Generator[Session, None, None]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()


@lru_cache()
def get_engine(blitz_app: "BlitzApp", db_type: DBTypes) -> Engine:
    match db_type:
        case DBTypes.SQLITE:
            return get_sqlite_engine(blitz_app)
        case DBTypes.MEMORY:
            return get_in_memory_engine()
        case DBTypes.POSTGRESQL:
            return get_postgresql_engine(blitz_app, settings=get_settings())
    raise ValueError("Unknown db type")


@contextmanager
def get_db(engine: Engine) -> Generator[Session, None, None]:
    with get_session(engine) as session:
        yield session
