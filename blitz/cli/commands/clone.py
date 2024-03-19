from json import JSONDecodeError
from typing import Annotated, Optional
from urllib.parse import urlparse
import requests
import typer
from blitz.cli.commands.create import BlitzProjectCreator
from blitz.cli.utils import progress
from blitz.models.blitz.file import BlitzFile, InvalidFileTypeError


def clone_project(
    url: Annotated[str, typer.Argument(help="URL of the project")],
    force: Annotated[bool, typer.Option(help="Don't check the URL validity")] = False,
    name: Annotated[Optional[str], typer.Option(help="Name of the project")] = None,
    format: Annotated[str, typer.Option(help="Format of the project")] = "yaml",
) -> None:
    parsed_url = urlparse(url)

    if force is False and not parsed_url.path.endswith("blitz-config"):
        print(f"Invalid URL: {url}")
        raise typer.Exit(1)

    with progress("Cloning Blitz App..."):
        try:
            blitz_file = BlitzFile.from_url(url, name, format=format)
        except (requests.HTTPError, JSONDecodeError):
            print(f"Failed to clone the project from {url}")
            raise typer.Exit(1)
        except InvalidFileTypeError as err:
            print(err)
            raise typer.Exit(1)

    name = name or blitz_file.config.name
    blitz_creator = BlitzProjectCreator(name, blitz_file.config.description, format, blitz_file, demo=False)

    blitz_creator.create_file_or_exit()
    blitz_creator.create_directory_or_exit()
    blitz_creator.print_success_message()
