from typing import Callable
from nicegui import ui
from blitz.ui.components.base import BaseComponent

from typing import Any


class BaseTimer(BaseComponent[ui.timer]):
    def __init__(
        self,
        interval: float,
        callback: Callable[..., Any],
        active: bool = True,
        once: bool = False,
        props: str = "",
        classes: str = "",
    ) -> None:
        self.interval = interval
        self.callback = callback
        self.active = active
        self.once = once
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = (
            ui.timer(self.interval, self.callback, once=self.once, active=self.active)
            .props(self.props)
            .classes(self.classes)
        )
