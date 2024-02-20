import contextlib
import time
from semver import Version
import typer
import os
import uvicorn

from pathlib import Path
from typing import Annotated, Optional
from uvicorn.supervisors import ChangeReload

from blitz.api import create_blitz_api
from blitz.cli.utils import print_version
from blitz.core import BlitzCore

from blitz.settings import get_settings
from blitz.cli.errors import (
    BlitzAppNotFoundError,
    BlitzAppVersionNotFoundError,
    MissingBlitzAppNameError,
)

from blitz import __version__


def start_blitz(
    blitz_app_name: Annotated[Optional[str], typer.Argument(help="Blitz app name")] = None,
    admin: Annotated[bool, typer.Option(help="Don't create admin.")] = True,
    port: Annotated[int, typer.Option(help="Define the port of the server")] = get_settings().BLITZ_PORT,
    config_route: Annotated[bool, typer.Option(help="Enable the blitz config route.")] = True,
    hot_reload: Annotated[bool, typer.Option(help="Enable the hot reload.")] = True,
    version: Annotated[Optional[str], typer.Option(help="Define the version of the app.")] = None,
) -> None:
    blitz = BlitzCore()

    if blitz_app_name is None:
        if len(blitz.apps) == 1:
            blitz_app = blitz.apps[0]
        else:
            raise MissingBlitzAppNameError()
    else:
        try:
            blitz_app = blitz.get_app(blitz_app_name)
        except Exception:
            raise BlitzAppNotFoundError(blitz_app_name)

    if version is not None:
        try:
            blitz_app = blitz_app.get_version(Version.parse(version))
        except Exception:
            raise BlitzAppVersionNotFoundError(blitz_app, version)

    # In case of error we don't want to stop the startup for ascii art.
    with contextlib.suppress(Exception):
        print_version(__version__)
        time.sleep(0.3)

    if hot_reload:
        # Need to be refacto
        os.environ["BLITZ_APP"] = str(blitz_app.name)
        if version is not None:
            os.environ["BLITZ_VERSION"] = str(version)
        os.environ["BLITZ_ADMIN"] = str(admin).lower()
        os.environ["BLITZ_CONFIG_ROUTE"] = str(config_route).lower()

        if blitz_app.file.path is None:
            # TODO: handle error
            raise Exception

        server_config = uvicorn.Config(
            "blitz.api:create_blitz_api",
            factory=True,
            host="localhost",
            port=port,
            reload=True,
            reload_includes=str(blitz_app.file.path.relative_to(Path.cwd())),
            reload_excludes=["*_migration.py", "migrations/*.py"],
            log_config=None,
            log_level="info",
        )
        server = uvicorn.Server(server_config)
        ChangeReload(server_config, target=server.run, sockets=[server_config.bind_socket()]).run()
    else:
        blitz_api = create_blitz_api(blitz_app, enable_config_route=config_route, admin=admin)
        uvicorn.run(blitz_api, host="localhost", port=port, log_config=None, log_level="warning")
