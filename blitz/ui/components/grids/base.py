from blitz.ui.components.base import BaseComponent
from nicegui import ui


class BaseGrid(BaseComponent[ui.grid]):
    def __init__(self, rows: int | None = None, columns: int | None = None, props: str = "", classes: str = "") -> None:
        self.ng: ui.grid
        self.rows = rows
        self.columns = columns
        super().__init__(props=props, classes=classes)

    def render(self) -> None:  # type: ignore
        self.ng = ui.grid(rows=self.rows, columns=self.columns).props(self.props).classes(self.classes)

class WFullGrid(BaseGrid.variant(classes="w-full")):  # type: ignore
    """Grid with w-full class."""