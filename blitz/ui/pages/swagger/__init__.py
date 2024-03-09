from pathlib import Path

from nicegui import ui

from blitz.ui.components.element.base import IFrame
from blitz.ui.pages.base import BasePage


class Page(BasePage):
    PAGE_NAME = "Swagger"

    def resize_iframe(self) -> None:
        with open(Path(__file__).parent / "./resize_iframe.js") as f:
            ui.run_javascript(f.read())

    def render(self) -> None:
        self.resize_iframe()
        self.ng = IFrame(
            src=f"{self.blitz_ui.settings.BLITZ_BASE_URL}/api/docs",
            frameborder=0,
            classes="w-full rounded-sm bg-white h-screen overflow-hidden",
            props="onload=resizeIframe()",
        )


SwaggerPage = Page
