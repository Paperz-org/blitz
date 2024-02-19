from typing import Any, Self
from blitz.ui.components.base import BaseComponent
from nicegui import ui
from starlette.requests import Request

from blitz.ui.components.header import FrameComponent


class BasePage(BaseComponent):
    PAGE_NAME = "Blitz Dashboard"
    FRAME: FrameComponent

    def __init__(self) -> None:
        super().__init__()
        self.setup()
        self.render()
        self.frame()

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if not hasattr(instance, "FRAME"):
            instance.FRAME = FrameComponent()
        return instance

    def frame(self) -> None:
        """The frame method HAVE to render a frame."""
        if self.FRAME is not None:
            self.FRAME.render()

    def setup(self) -> None:
        """The setup method is called before the render method."""
        pass

    def render(self) -> None:
        ui.label("Base Page")

    @classmethod
    def entrypoint(cls, request: Request) -> None:
        print(request.url.path)
        ui.page_title(cls.PAGE_NAME)
        cls()
