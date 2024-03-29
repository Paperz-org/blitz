from pathlib import Path
from nicegui import ui
from blitz.ui.pages.base import BasePage
from blitz.ui.components.buttons.icon import IconButton


class Page(BasePage):
    PAGE_NAME = "ERD"
    ZoomButton = IconButton.variant(classes="border rounded-sm")

    def setup(self) -> None:
        self._width = 100

    def remove_style(self) -> None:
        with open(Path(__file__).parent / "./remove_style.js") as f:
            ui.run_javascript(f.read())

    def zoom_svg(self) -> None:
        self._width += 50
        self.remove_style()
        # Can't put it in a file without a better integration like a bridge to js function or something like this
        ui.run_javascript(
            f"""
            var svg = document.querySelector('svg');
            svg.setAttribute("width", "{self._width}%");
            """
        )

    def unzoom_svg(self) -> None:
        self._width -= 50
        if self._width < 100:
            self._width = 100
        self.remove_style()
        # Can't put it in a file without a better integration like a bridge to js function or something like this
        ui.run_javascript(
            f"""
            var svg = document.querySelector('svg');
            svg.setAttribute("width", "{self._width}%");
            """
        )

    def render(self) -> None:
        with ui.scroll_area().classes("w-full h-screen justify-center content-center"):
            if self.blitz_ui.erd is None:
                # TODO handle error
                raise Exception
            ui.mermaid(self.blitz_ui.erd)
        with ui.footer().classes("w-full justify-start "):
            self.ZoomButton(icon="zoom_in", on_click=self.zoom_svg)
            self.ZoomButton(icon="zoom_out", on_click=self.unzoom_svg)


MermaidPage = Page
