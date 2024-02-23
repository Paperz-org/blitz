from nicegui import ui

from blitz.ui.components.base import BaseComponent


class BaseIcon(BaseComponent[ui.icon]):
    def __init__(
        self, name: str = "", size: str | None = None, color: str | None = None, props: str = "", classes: str = ""
    ) -> None:
        self.name = name
        self.size = size
        self.color = color
        super().__init__(props=props, classes=classes)
    
    def render(self) -> None:
        self.ng = ui.icon(name=self.name, size=self.size, color=self.color).props(self.props).classes(self.classes)



