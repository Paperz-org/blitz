from blitz.ui.components.header import FrameComponent
from blitz.ui.components.logger import LogComponent
from blitz.ui.pages.base import BasePage


class LogPage(BasePage):
    PAGE_NAME = "Log"

    def render(self) -> None:
        LogComponent().render()
