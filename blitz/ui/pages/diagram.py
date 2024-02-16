from nicegui import ui
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui


class MermaidPage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui(), project: str | None = None) -> None:
        self.project = project
        self.blitz_ui = blitz_ui
        self._width = 100

    def remove_style(self) -> None:
        ui.run_javascript(
            """
            var svg = document.querySelector('svg');
            svg.removeAttribute("style");
            """
        )

    def zoom_svg(self) -> None:
        self._width += 50
        self.remove_style()
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
        ui.run_javascript(
            f"""
            var svg = document.querySelector('svg');
            svg.setAttribute("width", "{self._width}%");
            """
        )

    def render_page(self) -> None:
        with ui.scroll_area().classes("w-full h-screen justify-center content-center"):
            if self.blitz_ui.erd is None:
                # TODO handle error
                raise Exception
            ui.mermaid(self.blitz_ui.erd)
        with ui.footer().classes("w-full justify-start "):
            ui.button(icon="zoom_in", on_click=self.zoom_svg).classes("borderrounded-sm").props("flat")
            ui.button(icon="zoom_out", on_click=self.unzoom_svg).classes("border rounded-sm").props("flat")
