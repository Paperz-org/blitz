from blitz.ui.components.buttons.flat import FlatButton
from .base import WFullLink
from nicegui import ui


class MenuLink(WFullLink):
    _FlatButton = FlatButton.variant(props="align=left", classes="px-4 hover:bg-slate-700 rounded-sm w-full")

    def __init__(self, label: str, link: str, icon: str) -> None:
        self.label = label
        self.link = link
        self.icon = icon
        super().__init__()

    def render(self) -> None:
        super().render()
        with self, self._FlatButton(on_click=self.go_to):
            ui.icon(name=self.icon, size="sm").props("flat").classes("pr-4")
            ui.label(self.label)

    def go_to(self) -> None:
        ui.open(self.link)
