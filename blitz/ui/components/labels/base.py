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


class BoldLabel(BaseLabel.variant(classes="font-bold")):  # type: ignore
    """Label with font-bold class."""


class TextXsLabel(BaseLabel.variant(classes="text-xs")):  # type: ignore
    """Label with text-xs class."""


class TextSmLabel(BaseLabel.variant(classes="text-sm")):  # type: ignore
    """Label with text-sm class."""


class TextMdLabel(BaseLabel.variant(classes="text-md")):  # type: ignore
    """Label with text-md class."""


class TextLgLabel(BaseLabel.variant(classes="text-lg")):  # type: ignore
    """Label with text-lg class."""


class TextXlLabel(BaseLabel.variant(classes="text-xl")):  # type: ignore
    """Label with text-xl class."""


class TextMdBoldLabel(BoldLabel, TextMdLabel):
    """Label with text-xs font-bold classes."""


class TextLgBoldLabel(BoldLabel, TextLgLabel):
    """Label with text-lg font-bold classes."""

class TextXlBoldLabel(BoldLabel, TextXlLabel):
    """Label with text-xl font-bold classes."""
