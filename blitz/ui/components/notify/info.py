from typing import Any
from nicegui import ui


def info(message: Any) -> None:
    ui.notify(message=message, type="info")
