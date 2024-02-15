from rich.console import Console
from rich.table import Table
from blitz.core import BlitzCore


from blitz.app import BlitzApp


def print_blitz_app(blitz_apps: list[BlitzApp]) -> None:
    console = Console()
    table = Table("Blitz app name", "Version")
    if len(blitz_apps) > 0:
        for blitz_app in blitz_apps:
            table.add_row(blitz_app.name, blitz_app.file.config.version)
    else:
        table.add_row("No blitz app found.")
    console.print(table)


def list_blitz_app() -> None:
    blitz = BlitzCore()
    print_blitz_app(blitz.apps)
