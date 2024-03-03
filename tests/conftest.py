import warnings
from typing import Any, get_type_hints

import pytest
import typeguard


# Adapted from https://github.com/untitaker/pytest-fixture-typecheck
def pytest_runtest_call(item: pytest.Function) -> None:
    try:
        annotations = get_type_hints(
            item.obj,
            globalns=item.obj.__globals__,
            localns={"Any": Any},  # pytest-bdd appears to insert an `Any` annotation
        )
    except TypeError:
        # get_type_hints may fail on Python <3.10 because pytest-bdd appears to have
        # `dict[str, str]` as a type somewhere, and builtin type subscripting isn't
        # supported yet
        warnings.warn(f"Type annotations could not be retrieved for {item.obj!r}", RuntimeWarning)
        return

    for attr, type_ in annotations.items():
        if attr in item.funcargs:
            try:
                typeguard.check_type(item.funcargs[attr], type_)
            except Exception as exc:
                raise pytest.UsageError(
                    f"Type of {attr!r} parameter in {item.name!r} function does not match its the type annotation: {type_!r}"
                ) from exc


pytest_plugins = (
    "tests.fixtures.app",
    "tests.fixtures.blitz",
    "tests.fixtures.cli",
    "tests.fixtures.runner",
)
