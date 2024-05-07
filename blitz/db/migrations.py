import logging
from argparse import Namespace
from pathlib import Path
from typing import TYPE_CHECKING

from alembic.command import check, revision, upgrade
from alembic.config import Config
from alembic.script import Script
from alembic.util import AutogenerateDiffsDetected

from blitz.db.errors import NoChangesDetectedError
from blitz.db.session import get_engine
from blitz.settings import get_settings

if TYPE_CHECKING:
    from blitz.app import BlitzApp


logging.getLogger("alembic").setLevel(logging.CRITICAL)

DEFAULT_MIGRATION_FILE_NAME_TEMPLATE = "%%(epoch)s_%%(rev)s"
RELEASE_MIGRATION_FILE_NAME_TEMPLATE = "migration"


def get_alembic_config(
    blitz_app: "BlitzApp",
    is_release: bool = False,
) -> Config:
    if is_release:
        file_name_template = RELEASE_MIGRATION_FILE_NAME_TEMPLATE
        migrations_paths = set(
            [str(blitz_app.path / str(version)) for version in blitz_app.versions]
            + [str(blitz_app.path / str(blitz_app.file.config.version))]
        )
    else:
        file_name_template = DEFAULT_MIGRATION_FILE_NAME_TEMPLATE
        migrations_paths = set([str(blitz_app.path / "migrations")])

    alembic_cfg = Config(cmd_opts=Namespace(quiet=True))
    # FIXME: Ugly way to find the alembic folder
    alembic_cfg.set_main_option("script_location", f"{Path(__file__).parent.parent.resolve()}/alembic")
    alembic_cfg.set_main_option("file_template", file_name_template)
    alembic_cfg.set_main_option("version_locations", " ".join(migrations_paths))
    alembic_cfg.set_main_option("recursive_version_locations", "true")

    return alembic_cfg


def generate_migration(
    message: str,
    blitz_app: "BlitzApp",
    is_release: bool = False,
) -> Path:
    # We attach the connection to the alembic config following the alembic sqlalchemy cookbook
    # https://alembic.sqlalchemy.org/en/latest/cookbook.html#sharing-a-connection-across-one-or-more-programmatic-migration-commands
    engine = get_engine(blitz_app, get_settings().BLITZ_DB_TYPE)
    with engine.begin() as connection:
        alembic_config = get_alembic_config(blitz_app=blitz_app, is_release=is_release)
        alembic_config.attributes["connection"] = connection
        alembic_config.attributes["sqlalchemy.url"] = connection.engine.url

        try:
            check(alembic_config)
        except AutogenerateDiffsDetected:
            if is_release:
                version_path = blitz_app.path / blitz_app.file.config.version
            else:
                version_path = blitz_app.path / "migrations"

            # Generate the migration
            migration = revision(
                alembic_config,
                message=message,
                autogenerate=True,
                version_path=str(version_path),
            )
            if isinstance(migration, Script):
                return Path(migration.path)
            else:
                raise Exception("Too many migration generated.")
        else:
            raise NoChangesDetectedError("No migration to generate.")


def run_migrations(
    blitz_app: "BlitzApp",
    is_release: bool = False,
) -> None:
    # We attach the connection to the alembic config following the alembic sqlalchemy cookbook
    # https://alembic.sqlalchemy.org/en/latest/cookbook.html#sharing-a-connection-across-one-or-more-programmatic-migration-commands
    with get_engine(blitz_app, get_settings().BLITZ_DB_TYPE).begin() as connection:
        alembic_config = get_alembic_config(blitz_app=blitz_app, is_release=is_release)
        alembic_config.attributes["connection"] = connection
        alembic_config.attributes["sqlalchemy.url"] = connection.engine.url

        upgrade(alembic_config, revision="head")
