from nicegui import ui
from typing import Callable
from blitz.ui.components.base import BaseComponent


class BaseExpansion(BaseComponent[ui.expansion]):
    def __init__(
        self,
        text: str = "",
        caption: str | None = None,
        icon: str | None = None,
        group: str | None = None,
        value: bool = False,
        on_value_change: Callable[..., None] | None = None,
        props: str = "",
        classes: str = "",
    ) -> None:
        self.text = text
        self.caption = caption
        self.icon = icon
        self.group = group
        self.value = value
        self.on_value_change = on_value_change
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = (
            ui.expansion(
                self.text,
                caption=self.caption,
                icon=self.icon,
                group=self.group,
                value=self.value,
                on_value_change=self.on_value_change,
            )
            .classes(self.classes)
            .props(self.props)
        )


class BaseAccordion(BaseExpansion):
    def __init__(
        self,
        text: str = "",
        caption: str | None = None,
        icon: str | None = None,
        group: str | None = None,
        is_open: bool = False,
        on_change: Callable[..., None] | None = None,
        props: str = "",
        classes: str = "",
    ) -> None:
        super().__init__(
            text=text,
            caption=caption,
            icon=icon,
            group=group,
            value=is_open,
            on_value_change=on_change,
            props=props,
            classes=classes,
        )