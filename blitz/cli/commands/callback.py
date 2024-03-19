from typing import Annotated, Optional
import typer
from blitz import __version__

def version_callback(show_version: bool) -> None:
    if show_version:
        print(__version__)

def callback(version: Annotated[Optional[bool], typer.Option("--version", help="Show the Blitz version.", callback=version_callback)] = None) -> None:
    if version:
        print(__version__)
