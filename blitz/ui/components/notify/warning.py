from typing import Any
from nicegui import ui


def warning(message: Any) -> None:
    ui.notify(message=message, type="warning")
