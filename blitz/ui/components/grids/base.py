from blitz.ui.components.base import BaseComponent
from nicegui import ui

ui.grid(rows=2, columns=2).classes("gap-4")


class BaseGrid(BaseComponent[ui.grid]):
    def __init__(self, rows: int | None = None, columns: int | None = None, props: str = "", classes: str = "") -> None:
        self.rows = rows
        self.columns = columns
        super().__init__(props=props, classes=classes)

    def render(self) -> None:  # type: ignore
        self.ng = ui.grid(rows=self.rows, columns=self.columns).props(self.props).classes(self.classes)


