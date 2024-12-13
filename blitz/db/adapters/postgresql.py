from typing import TYPE_CHECKING

from sqlalchemy import Engine

from blitz.db.engine import create_engine
from blitz.settings import Settings

if TYPE_CHECKING:
    from blitz.app import BlitzApp


def get_postgresql_engine(
    blitz_app: "BlitzApp",
    settings: Settings,
) -> Engine:
    schema_name = blitz_app.name
    assert settings.POSTGRES
    # FIXME find more elegant implementation
    url = f"postgresql+psycopg2://{settings.POSTGRES.USER}:{settings.POSTGRES.PASSWORD}@{settings.POSTGRES.HOST}:{settings.POSTGRES.PORT}/{schema_name}"
    engine = create_engine(url)
    return engine
