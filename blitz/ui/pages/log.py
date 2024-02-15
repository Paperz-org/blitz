from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components.logger import LogComponent


class LogPage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui

    def render_page(self) -> None:
        LogComponent().render()
