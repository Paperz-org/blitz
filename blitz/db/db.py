from sqlmodel import Session, create_engine
from typing import Any, Generator
from functools import lru_cache
from sqlalchemy import Engine, event
from sqlalchemy import pool
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from blitz.app import BlitzApp


def _fk_pragma_on_connect(dbapi_con: Any, con_record: Any) -> None:
    """
    Enable foreign keys on SQLite.
    """
    dbapi_con.execute("pragma foreign_keys=ON")


@lru_cache
def get_engine(url: str) -> Engine:
    return create_engine(url, connect_args={"check_same_thread": False}, poolclass=pool.StaticPool)


# FIXME find how to avoid that
@lru_cache
def get_sqlite_engine(
    blitz_app: "BlitzApp",
    in_memory: bool,
    file_name: str,
) -> Engine:
    # TODO find a better implementation
    if blitz_app.version:
        file_name = f"{blitz_app.version}/{file_name}"

    if in_memory is True:
        url = "sqlite://"
    else:
        url = f"sqlite:///{blitz_app.path.absolute()}/{file_name}"
    engine = get_engine(url)
    event.listen(engine, "connect", _fk_pragma_on_connect)
    return engine


def get_db(blitz_app: "BlitzApp", in_memory: bool, file_name: str) -> Generator[Session, None, None]:
    with Session(get_sqlite_engine(blitz_app, in_memory, file_name)) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
        finally:
            session.close()
