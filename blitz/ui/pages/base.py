from typing import Any, Self

from nicegui import ui
from starlette.requests import Request

from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components.header import FrameComponent
from blitz.ui.components.labels import Label


class BasePage:
    PAGE_NAME = "Blitz Dashboard"
    FRAME: FrameComponent

    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui
        self.current_project = self.blitz_ui.current_project
        self.current_app = self.blitz_ui.current_app

        self.setup()
        super().__init__()
        self.render()

    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls, *args, **kwargs)
        if not hasattr(instance, "FRAME"):
            instance.FRAME = FrameComponent()
        return instance

    # def frame(self) -> None:
    #     """The frame method HAVE to render a frame."""
    #     if self.FRAME is not None:
    #         self.FRAME

    def setup(self) -> None:
        """The setup method is called before the render method."""
        pass

    def render(self) -> None:
        Label("Base Page")

    @classmethod
    def entrypoint(cls, request: Request) -> None:
        ui.page_title(cls.PAGE_NAME)
        cls()
