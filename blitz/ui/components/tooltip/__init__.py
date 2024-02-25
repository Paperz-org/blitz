
from nicegui import ui
from blitz.ui.components.base import BaseComponent


class Tooltip(BaseComponent[ui.tooltip]):
    def __init__(self, text: str, props: str = "", classes: str = "") -> None:
        self.text = text
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = ui.tooltip(self.text).props(self.props).classes(self.classes)