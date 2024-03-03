from typing import Any
from nicegui import ui


def success(message: Any) -> None:
    ui.notify(message=message, type="positive")
