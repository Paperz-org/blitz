from pathlib import Path
from typing import Annotated, Literal

import pytest

from tests.fixtures.cli import HANDLED_ERROR_EXIT_CODE, OK_EXIT_CODE, Cli


def check_blitz_app_structure(blitz_app_path: Path, file_format: Annotated[str, Literal["json", "yaml"]]) -> None:
    assert blitz_app_path.exists()
    assert blitz_app_path.is_dir()
    assert (blitz_app_path / f"blitz.{file_format}").exists()
    assert (blitz_app_path / ".blitz").exists()


@pytest.mark.parametrize("file_format", ["json", "yaml"])
def test_create_blitz_app(cli: Cli, file_format: str) -> None:
    blitz_app_name = "test"
    t = cli.create(blitz_app_name=blitz_app_name, input_description="test", input_file_format=file_format)
    blitz_app_path = cli.working_path / blitz_app_name
    check_blitz_app_structure(blitz_app_path, file_format)
    assert t.exit_code == OK_EXIT_CODE


@pytest.mark.parametrize("file_format", ["json", "yaml"])
def test_already_existing_blitz_app(cli: Cli, file_format: str) -> None:
    blitz_app_name = "test"
    t = cli.create(blitz_app_name=blitz_app_name, input_description="test", input_file_format=file_format)
    assert t.exit_code == OK_EXIT_CODE
    t = cli.create(blitz_app_name=blitz_app_name, input_description="test", input_file_format=file_format)
    assert t.exit_code == HANDLED_ERROR_EXIT_CODE


def test_create_demo_blitz_app(cli: Cli) -> None:
    t = cli.create(demo=True)
    blitz_app_path = cli.working_path / "demo-blitz-app"
    check_blitz_app_structure(blitz_app_path, "yaml")
    assert t.exit_code == OK_EXIT_CODE
