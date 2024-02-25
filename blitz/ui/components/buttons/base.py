from typing import Any
from nicegui import ui
from blitz.ui.components.base import BaseComponent


class BaseButton(BaseComponent[ui.button]):
    def __init__(
        self,
        text: str = "",
        *,
        on_click: Any | None = None,
        color: str | None = "primary",
        icon: str | None = None,
        props: str = "",
        classes: str = "",
        **kwargs: Any,
    ) -> None:
        self.text = text
        self.on_click = on_click
        self.color = color
        self.icon = icon
        super().__init__(props=props, classes=classes, **kwargs)

    def render(self) -> None:
        self.ng = (
            ui.button(
                self.text,
                on_click=self.on_click,
                color=self.color,
                icon=self.icon,
            )
            .props(self.props)
            .classes(self.classes)
        )
