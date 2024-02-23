from typing import Any
from blitz.ui.components.base import BaseComponent
from nicegui import ui


class BaseLabel(BaseComponent[ui.label]):
    def __init__(self, text: str = "", props: str = "", classes: str = "") -> None:
        self.text = text
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = ui.label(self.text).props(self.props).classes(self.classes)


class RedLabel(BaseLabel.variant(classes="text-red")):  # type: ignore
    """Label with text-red-500 class."""


class LGFontBoldLabel(BaseLabel.variant(classes="text-lg font-bold")):  # type: ignore
    """Label with text-lg font-bold classes."""
