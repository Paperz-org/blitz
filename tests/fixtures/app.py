from typing import Iterator

import pytest
from typer import Typer

from blitz.cli import app as _app


@pytest.fixture
def app() -> Iterator[Typer]:
    yield _app
