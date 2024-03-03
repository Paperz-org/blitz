from pathlib import Path

from nicegui import ui

from blitz.ui.components import Component


class Image(Component[ui.image]):
    def __init__(self, src: str | Path, props: str = "", classes: str = "") -> None:
        self.src = src
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = ui.image(self.src).props(self.props).classes(self.classes)
