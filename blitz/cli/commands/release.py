from typing import Annotated, Optional
from blitz import BlitzCore
from blitz.app import ReleaseLevel
import typer
from rich import print

from blitz.db.errors import NoChangesDetectedError as MigrationNoChangesDetectedError
from blitz.cli.errors import BlitzAppNotFoundError, MissingBlitzAppNameError, NoChangesDetectedError


def release_blitz(
    blitz_app_name: Annotated[Optional[str], typer.Argument(help="Blitz app to release")] = None,
    force: Annotated[bool, typer.Option(help="Force the release even if no changes are detected")] = False,
    patch: Annotated[bool, typer.Option(help="Release level patch")] = False,
    minor: Annotated[bool, typer.Option(help="Release level minor")] = False,
    major: Annotated[bool, typer.Option(help="Release level major")] = False,
) -> None:
    # Can't have both --patch and --minor or --major
    if sum([patch, minor, major]) > 1:
        raise typer.BadParameter("You can't use more than one release level")
    release_level = ReleaseLevel.MAJOR if major else ReleaseLevel.MINOR if minor else ReleaseLevel.PATCH

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

    try:
        new_version = blitz_app.release(release_level, force=force)
    except MigrationNoChangesDetectedError:
        raise NoChangesDetectedError()

    print(f"Blitz app {blitz_app.name} released at version {new_version}")
    print("You can now start your versioned blitz app by running:")
    print(f"    [bold medium_purple1]blitz start {blitz_app.name} --version {new_version}[/bold medium_purple1]")
