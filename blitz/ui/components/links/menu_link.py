from blitz.ui.components.buttons.flat import FlatButton
from .base import WFullLink
from blitz.ui.components.labels import Label
from nicegui import ui


class MenuLink(WFullLink):
    _FlatButton = FlatButton.variant(props="align=left", classes="px-4 hover:bg-slate-700 rounded-sm w-full")

    def __init__(self, label: str, link: str, icon: str | None = None) -> None:
        self.label = label
        self.link = link
        self.icon = icon
        super().__init__()

    def render(self) -> None:
        super().render()
        with self, self._FlatButton(on_click=self.go_to):
            if self.icon is not None:
                ui.icon(name=self.icon, size="sm").props("flat").classes("pr-4")
            Label(self.label)

    def go_to(self) -> None:
        ui.open(self.link)
