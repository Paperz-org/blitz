from typing import Annotated
from blitz import BlitzCore
import typer
from rich import print
import enum

from blitz.db.errors import NoChangesDetectedError


class ReleaseLevel(enum.Enum):
    major = "major"
    minor = "minor"
    patch = "patch"


def release_blitz(
    blitz_app_name: Annotated[str, typer.Argument(..., help="Blitz app to release")],
    level: Annotated[ReleaseLevel, typer.Argument(..., help="Release level")],
    force: Annotated[bool, typer.Option(help="Force the release even if no changes are detected")] = False,
) -> None:
    blitz = BlitzCore()

    app = blitz.get_app(blitz_app_name)
    try:
        new_version = app.release(level.value, force=force)
    except NoChangesDetectedError:
        typer.echo(f"No changes detected since the latest version. Use --force to release anyway.")
        raise typer.Exit(code=1)
    typer.echo(f"Blitz app {blitz_app_name} released at version {new_version}")
    typer.echo("You can now start your versioned blitz app by running:")
    print(f"    [bold medium_purple1]blitz start {blitz_app_name} --version {new_version}[/bold medium_purple1]")
