from pathlib import Path
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from nicegui import ui

from blitz.ui.components.element.base import IFrame


class Page:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui

    def resize_iframe(self) -> None:
        with open(Path(__file__).parent / "./resize_iframe.js") as f:
            ui.run_javascript(f.read())

    def render_page(self) -> None:
        self.resize_iframe()
        self.ng = IFrame(
            src=f"{self.blitz_ui.localhost_url}/admin/",
            frameborder=0,
            classes="w-full rounded-sm bg-white h-screen overflow-hidden",
            props="onload=resizeIframe()",
        )


AdminPage = Page
