from nicegui import ui

from blitz.ui.components.base import BaseComponent


class BaseRow(BaseComponent[ui.row]):
    def __init__(self, wrap: bool = True, props: str = "", classes: str = "") -> None:
        self.wrap = wrap
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = ui.row(wrap=self.wrap).props(self.props).classes(self.classes)


class WFullRow(BaseRow.variant(classes="w-full")):  # type: ignore
    """Row with w-full class."""


class ContentCenterRow(BaseRow.variant(classes="content-center")):  # type: ignore
    """Row with content-center class."""


class ItemsCenterRow(BaseRow.variant(classes="items-center")):  # type: ignore
    """Row with items-center class."""


class JustifyBetweenRow(BaseRow.variant(classes="justify-between")):  # type: ignore
    """Row with justify-between class."""


class WFullItemsCenterRow(WFullRow, ItemsCenterRow):
    """Row with w-full and items-center classes."""


class WFullContentCenterRow(WFullRow, ContentCenterRow):
    """Row with w-full and content-center classes."""

class WFullSpaceBetweenRow(WFullRow, JustifyBetweenRow, ItemsCenterRow):
    """Row with w-full and space-between classes."""

class ItemsCenterContentCenterRow(ItemsCenterRow, ContentCenterRow):
    """Row with items-center and content-center classes."""
