from typing import Iterator

import pytest
from typer.testing import CliRunner


@pytest.fixture
def runner() -> Iterator[CliRunner]:
    yield CliRunner()
