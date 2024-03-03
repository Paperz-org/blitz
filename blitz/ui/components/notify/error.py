from nicegui import ui


def error(message: str) -> None:
    ui.notify(message, type="negative")
