import typer
from rich import print

from blitz.app import BlitzApp


class BlitzCLIError(typer.Exit):
    CODE = 1


class BlitzAppNotFoundError(BlitzCLIError):
    def __init__(self, blitz_app_name: str) -> None:
        self.blitz_app_name = blitz_app_name
        print(f"[red bold]There is no blitz app named {blitz_app_name}[/red bold]")
        print("To list the available blitz apps run:")
        print("[bold]    blitz list[bold]")
        super().__init__(code=self.CODE)


class BlitzAppVersionNotFoundError(BlitzCLIError):
    def __init__(self, blitz_app: BlitzApp, version: str) -> None:
        self.blitz_app = blitz_app
        self.version = version
        print(f"[red bold]There is no version {version} for the blitz app {blitz_app.name}[/red bold]")
        print("Available versions are:")
        for blitz_app_version in blitz_app.versions:
            print(f"    {blitz_app_version}")
        super().__init__(code=self.CODE)


class MissingBlitzAppNameError(BlitzCLIError):
    def __init__(self) -> None:
        print("You need to specify a blitz app name.")
        print("To list the available blitz apps run:")
        print("[bold]    blitz list[bold]")
        super().__init__(code=self.CODE)


class NoChangesDetectedError(BlitzCLIError):
    def __init__(self) -> None:
        print("No changes detected since the latest version. Use --force to release anyway.")
        super().__init__(code=self.CODE)