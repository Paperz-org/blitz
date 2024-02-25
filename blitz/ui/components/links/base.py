from typing import Any
from blitz.ui.components.base import BaseComponent
from nicegui import ui
from nicegui.element import Element


class BaseLink(BaseComponent[ui.link]):
    def __init__(
        self, text: str = "", target: str | Element = "#", new_tab: bool = False, props: str = "", classes: str = ""
    ) -> None:
        self.text = text
        self.target = target
        self.new_tab = new_tab
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = (
            ui.link(text=self.text, target=self.target, new_tab=self.new_tab).props(self.props).classes(self.classes)
        )


class WFullLink(BaseLink.variant(classes="w-full")):  # type: ignore
    """Link with w-full class."""
