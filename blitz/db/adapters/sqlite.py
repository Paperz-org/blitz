# FIXME find how to avoid that
from functools import lru_cache
from typing import TYPE_CHECKING, Any

from sqlalchemy import Engine, event

from blitz.db.engine import create_engine

if TYPE_CHECKING:
    from blitz.app import BlitzApp


# FIXME: fix typing
def _fk_pragma_on_connect(dbapi_con: Any, con_record: Any) -> None:
    """
    Enable foreign keys on SQLite.
    """
    dbapi_con.execute("pragma foreign_keys=ON")


def get_sqlite_engine(
    blitz_app: "BlitzApp",
    db_file_name: str = "app.db",
) -> Engine:
    if blitz_app.version:
        url = f"sqlite:///{blitz_app.path.absolute()}/{blitz_app.version}/{db_file_name}"
    else:
        url = f"sqlite:///{blitz_app.path.absolute()}/{db_file_name}"

    engine = create_engine(url, check_same_thread=False)
    event.listen(engine, "connect", _fk_pragma_on_connect)
    return engine
