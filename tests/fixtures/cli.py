from enum import StrEnum
from pathlib import Path
from typing import Annotated, Iterator, Literal, overload

import pytest
from click.testing import Result
from typer import Typer
from typer.testing import CliRunner

OK_EXIT_CODE = 0
HANDLED_ERROR_EXIT_CODE = 1


class Commands(StrEnum):
    CREATE = "create"
    START = "start"


class Cli:
    def __init__(self, app: Typer, runner: CliRunner, working_path: Path) -> None:
        self.app = app
        self.runner = runner
        self.working_path = working_path

    def _process_result(self, result: Result) -> None:
        print(result.stdout)

    @overload
    def create(
        self,
        *,
        blitz_app_name: None = None,
        input_blitz_app_name: str,
        input_description: str,
        input_file_format: Annotated[str, Literal["json", "yaml"]],
        demo: bool = False,
    ) -> Result:
        ...

    @overload
    def create(
        self,
        *,
        blitz_app_name: str,
        input_blitz_app_name: None = None,
        input_description: str,
        input_file_format: Annotated[str, Literal["json", "yaml"]],
        demo: bool = False,
    ) -> Result:
        ...

    @overload
    def create(
        self,
        *,
        blitz_app_name: None = None,
        input_blitz_app_name: None = None,
        input_description: None = None,
        input_file_format: None = None,
        demo: bool = True,
    ) -> Result:
        ...

    def create(
        self,
        *,
        blitz_app_name: str | None = None,
        input_blitz_app_name: str | None = None,
        input_description: str | None = None,
        input_file_format: Annotated[str, Literal["json", "yaml"]] | None = None,
        demo: bool = False,
    ) -> Result:
        args = []
        if blitz_app_name:
            args.append(blitz_app_name)
        if demo:
            args.append("--demo")

        user_inputs = []
        if input_blitz_app_name:
            user_inputs.append(input_blitz_app_name)
        if input_description is not None:
            user_inputs.append(input_description)
        if input_file_format is not None:
            user_inputs.append(input_file_format)

        result = self.runner.invoke(
            self.app,
            [Commands.CREATE] + args,
            input="\n".join(user_inputs) + "\n",
        )
        self._process_result(result)
        return result

    def start(
        self,
        *,
        blitz_app_name: str | None,
        admin: bool = True,
        port: int = 8100,
        config_route: bool = True,
        hot_reload: bool = True,
        version: str | None = None,
    ) -> Result:
        args = []
        if blitz_app_name:
            args.append(blitz_app_name)
        args.append("--port")
        args.append(str(port))
        if not admin:
            args.append("--no-admin")
        if not config_route:
            args.append("--no-config-route")
        if not hot_reload:
            args.append("--no-hot-reload")
        if version:
            args.append("--version")
            args.append(version)
        result = self.runner.invoke(self.app, [Commands.START] + args)
        self._process_result(result)
        return result


@pytest.fixture
def cli(
    app: Typer,
    runner: CliRunner,
    tmp_path: Annotated[Path, pytest.fixture],
) -> Iterator[Cli]:
    with runner.isolated_filesystem(temp_dir=tmp_path) as working_path:
        yield Cli(app, runner, Path(working_path))
