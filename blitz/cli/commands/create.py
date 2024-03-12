from pathlib import Path
from typing import Annotated, Optional

import typer
import yaml
from rich import print, prompt

from blitz.models.blitz.config import BlitzAppConfig
from blitz.models.blitz.file import BlitzFile
from blitz.models.blitz.resource import BlitzResourceConfig


def get_blitz_demo_resources() -> list[BlitzResourceConfig]:
    return [
        BlitzResourceConfig(
            name="Food",
            fields={
                "name!": "str!",
                "expiration_date": "datetime!",
            },
        ),
        BlitzResourceConfig(
            name="Ingredient",
            fields={
                "food_id": "Food.id",
                "food": "Food",
                "recipe_id": "Recipe.id!",
                "recipe": "Recipe",
            },
        ),
        BlitzResourceConfig(
            name="Recipe",
            fields={
                "name!": "str!",
                "ingredients": "Ingredient[]",
                "cook_id": "Cook.id!",
                "cook": "Cook",
            },
        ),
        BlitzResourceConfig(
            name="Cook",
            fields={
                "name!": "str!",
                "age": "int!",
                "recipes": "Recipe[]",
                "rat": "Rat",
            },
        ),
        BlitzResourceConfig(
            name="Rat",
            fields={
                "name!": "str!",
                "age": "int!",
                "cook_id!": "Cook.id!",
                "cook": "Cook",
            },
        ),
    ]


class BlitzCreator:
    pass


class BlitzProjectCreator:
    DEFAULT_VERSION = "0.1.0"
    DEFAULT_BLITZ_APP_NAME = "Random Blitz App"
    DEFAULT_BLIZ_APP_DESCRIPTION = ""
    DEFAULT_BLITZ_FILE_FORMAT = "json"
    DEMO_BLITZ_APP_DESCRIPTION = "This is a demo blitz app"
    DEMO_BLITZ_APP_NAME = "Demo Blitz App"

    def __init__(
        self,
        name: str,
        description: str | None,
        file_format: str,
        blitz_file: BlitzFile | None = None,
        demo: bool = False,
    ) -> None:
        self.name = name
        self.description = description or ""
        self.file_format = file_format
        self.path = Path(self.name.lower().replace(" ", "-"))
        self.demo = demo

        self.blitz_file = blitz_file

    def create_directory_or_exit(self) -> None:
        if not self.blitz_file:
            self.create_file_or_exit()
        try:
            # Create the blitz app directory, the .blitz file and the blitz file
            self._create_directory()
        except Exception as e:
            self._print_directory_error(e)
            raise typer.Exit(code=1)

    def create_file_or_exit(self) -> None:
        try:
            # Create the blitz file
            self._create_file()
        except Exception as e:
            self._print_file_error(e)
            raise typer.Exit(code=1)

    def print_success_message(self) -> None:
        print(f"\n[medium_purple1 bold]{self.name}[/medium_purple1 bold] created successfully !")
        print("To start your app, you can use:")
        print(f"    [bold medium_purple1]blitz start {self.path}[/bold medium_purple1]")

    def _create_directory(self) -> None:
        self.path.mkdir(parents=True)
        blitz_app_file_path = self.path / ".blitz"
        blitz_app_file_path.touch()
        blitz_file_path = self._write_blitz_file()
        with open(blitz_app_file_path, "w") as blitz_app_file:
            blitz_app_file.write(str(blitz_file_path))

    def _create_file(self) -> None:
        if not self.blitz_file:
            self.blitz_file = BlitzFile(
                path=self.path / f"blitz.{self.file_format}",
                config=BlitzAppConfig(
                    name=self.name,
                    description=self.description,
                    version=self.DEFAULT_VERSION,
                ),
                resources_configs=get_blitz_demo_resources() if self.demo else [],
                raw_file={},
            )

    def _write_blitz_file(self) -> Path:
        if self.blitz_file is None:
            # TODO Handle error
            raise Exception()
        match self.file_format:
            case "json":
                blitz_file_data = self.blitz_file.model_dump_json(indent=4, by_alias=True, exclude_unset=True)
            case "yaml":
                blitz_file_data = yaml.dump(
                    self.blitz_file.model_dump(by_alias=True, exclude_unset=True),
                    default_flow_style=False,
                )
            case _:
                raise ValueError("Invalid blitz file format")

        if self.blitz_file.path is None:
            # TODO: handle error
            raise Exception("toto")
        with open(self.blitz_file.path, "w") as file:
            file.write(blitz_file_data)
        return self.blitz_file.path

    @staticmethod
    def _print_file_error(error: Exception) -> None:
        print(f"[red bold]Error[/red bold] while creating the blitz file: {error}")

    @staticmethod
    def _print_directory_error(error: Exception) -> None:
        print(f"[red bold]Error[/red bold] while creating the blitz app in the file system: {error}")


def create_blitz_app(
    blitz_app_name: Annotated[
        Optional[str],
        typer.Argument(help="The name of the blitz app you want to create"),
    ] = None,
    demo: Annotated[bool, typer.Option(help="Create a demo blitz app")] = False,
) -> None:
    name = blitz_app_name
    if demo:
        name = BlitzProjectCreator.DEMO_BLITZ_APP_NAME
        description = BlitzProjectCreator.DEMO_BLITZ_APP_DESCRIPTION
        file_format = BlitzProjectCreator.DEFAULT_BLITZ_FILE_FORMAT
    else:
        if not name:
            # Interactive prompt to create a new blitz app
            name = prompt.Prompt.ask(
                "Enter the name of your blitz app",
                default=BlitzProjectCreator.DEFAULT_BLITZ_APP_NAME,
            )
        description = prompt.Prompt.ask(
            "Enter the description of your blitz app",
            default=BlitzProjectCreator.DEFAULT_BLIZ_APP_DESCRIPTION,
        )
        file_format = prompt.Prompt.ask(
            "Choose the format of the blitz file (can be changed later)",
            choices=["json", "yaml"],
            default=BlitzProjectCreator.DEFAULT_BLITZ_FILE_FORMAT,
        )

    blitz_creator = BlitzProjectCreator(name, description, file_format, demo=demo)
    blitz_creator.create_file_or_exit()
    blitz_creator.create_directory_or_exit()
    blitz_creator.print_success_message()
