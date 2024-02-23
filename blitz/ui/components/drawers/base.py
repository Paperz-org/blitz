from nicegui import ui

from blitz.ui.components.base import BaseComponent


class BaseLeftDrawer(BaseComponent[ui.left_drawer]):
    def __init__(
        self,
        value: bool | None = None,
        fixed: bool = True,
        bordered: bool = False,
        elevated: bool = False,
        top_corner: bool = False,
        bottom_corner: bool = False,
        props: str = "",
        classes: str = "",
    ) -> None:
        self.value = value
        self.fixed = fixed
        self.bordered = bordered
        self.elevated = elevated
        self.top_corner = top_corner
        self.bottom_corner = bottom_corner
        super().__init__(props=props, classes=classes)

    def toggle(self) -> None:
        self.ng.toggle()

    def show(self) -> None:
        self.ng.show()

    def hide(self) -> None:
        self.ng.hide()

    def render(self) -> None:
        self.ng = (
            ui.left_drawer(
                value=self.value,
                fixed=self.fixed,
                bordered=self.bordered,
                elevated=self.elevated,
                top_corner=self.top_corner,
                bottom_corner=self.bottom_corner,
            )
            .props(self.props)
            .classes(self.classes)
        )
