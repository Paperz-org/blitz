from pathlib import Path
from typing import Annotated, Optional
from rich import prompt, print
from blitz.models.blitz.file import BlitzFile
import yaml
from blitz.models.blitz.config import BlitzAppConfig
import typer

DEFAULT_VERSION = "0.1.0"


def write_blitz_file(blitz_file: BlitzFile, blitz_file_format: str) -> Path:
    if blitz_file_format == "json":
        blitz_file_data = blitz_file.model_dump_json(indent=4, by_alias=True)
    elif blitz_file_format == "yaml":
        blitz_file_data = yaml.dump(blitz_file.model_dump(by_alias=True), default_flow_style=False)
    else:
        raise ValueError("Invalid blitz file format")

    with open(blitz_file.path, "w") as file:
        file.write(blitz_file_data)

    return blitz_file.path


def create_blitz_app(
    blitz_app_name: Annotated[
        Optional[str], typer.Argument(help="The name of the blitz app you want to create")
    ] = None,
) -> None:
    if not blitz_app_name:
        # Interactive prompt to create a new blitz app
        blitz_app_name = prompt.Prompt.ask(
            "Enter the name of your blitz app",
            default="Random Blitz App",
        )
    blitz_app_description = prompt.Prompt.ask(
        "Enter the description of your blitz app",
        default="",
    )
    blitz_file_format = prompt.Prompt.ask(
        "Choose the format of the blitz file (can be changed later)",
        choices=["json", "yaml"],
        default="yaml",
    )

    blitz_app_path = Path(blitz_app_name.lower().replace(" ", "-"))
    try:
        # Create the blitz file
        blitz_file = BlitzFile(
            path=blitz_app_path / f"blitz.{blitz_file_format}",
            config=BlitzAppConfig(
                name=blitz_app_name,
                description=blitz_app_description,
                version=DEFAULT_VERSION,
            ),
            resources_configs=[],
            raw_file={},
        )
    except Exception as e:
        print(f"[red bold]Error[/red bold] while creating the blitz file: {e}")
        typer.Exit(code=1)
    try:
        # Create the blitz app directory, the .blitz file and the blitz file
        blitz_app_path.mkdir(parents=True)
        blitz_app_file_path = blitz_app_path / ".blitz"
        blitz_app_file_path.touch()
        blitz_file_path = write_blitz_file(blitz_file, blitz_file_format)
        with open(blitz_app_file_path, "w") as blitz_app_file:
            blitz_app_file.write(str(blitz_file_path))
    except Exception as e:
        print(f"[red bold]Error[/red bold] while creating the blitz app in the file system: {e}")
        typer.Exit(code=1)

    print(f"\n[medium_purple1 bold]{blitz_app_name}[/medium_purple1 bold] created successfully !")
    print("To start your app, you can use:")
    print(f"    [bold medium_purple1]blitz start {blitz_app_path}[/bold medium_purple1]")
