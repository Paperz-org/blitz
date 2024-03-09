import time
from multiprocessing import Process
from pathlib import Path
from typing import Iterator

import httpx
import pytest

from tests.fixtures.cli import Cli


@pytest.fixture
def blitz_app_path(cli: Cli) -> Iterator[Path]:
    # Find a way to not depends of that
    cli.create(demo=True)
    yield cli.working_path / "demo-blitz-app"


@pytest.fixture
def blitz_app(cli: Cli, blitz_app_path: Path) -> Iterator[None]:
    proc = Process(
        target=cli.start,
        kwargs={"blitz_app_name": blitz_app_path.name, "hot_reload": False},
    )
    try:
        proc.start()
        with httpx.Client() as client:
            maximum_try = 0
            while maximum_try < 20:
                maximum_try += 1
                try:
                    response = client.get("http://0.0.0.0:8100/api/docs")
                    response.raise_for_status()
                except Exception:
                    time.sleep(0.2)
                    continue
                break
            else:
                raise RuntimeError("Server starts but is not reachable.")
        yield
    finally:
        proc.terminate()
        proc.kill()
