from pathlib import Path

from nicegui import ui
from blitz.ui.components.buttons import FlatButton
from blitz.ui.components.base import BaseComponent
from blitz.ui.components.drawers.dashboard import DashboardDrawer
from blitz.ui.components.rows import ItemsCenterContentCenterRow

MAIN_PINK = "#cd87ff"
DARK_PINK = "#a72bff"


class HeaderComponent(BaseComponent[ui.header], reactive=True):
    def __init__(
        self,
        title: str = "",
        drawer: DashboardDrawer | None = None,
    ) -> None:
        self.drawer = drawer
        self.title = title

        self.dark_mode = ui.dark_mode(value=True)
        self.home_link = (
            f"dashboard/projects/{self.blitz_ui.current_project}" if self.blitz_ui.current_project else "projects"
        )
        ui.add_head_html(f"<style>{(Path(__file__).parent.parent / 'static' / 'style.css').read_text()}</style>")

        ui.add_head_html(
            f"<style>{(Path(__file__).parent.parent / 'static' / 'jse_theme_dark.css').read_text()}</style>"
        )

        ui.colors(
            primary="fffafa",
            secondary="#a72bff",
            accent="#111B1E",
            positive="#53B689",
            dark="#3e3e42",
        )
        super().__init__()

    def render(self) -> None:
        with ui.header(bordered=True).classes("pl-1 pr-8 justify-between content-center h-16 backdrop-blur-sm"):
            with ui.row().classes("items-center space-x-20 content-center my-auto"):
                with ui.row().classes("items-center space-x-0 content-center "):
                    if self.drawer is not None:
                        FlatButton(icon="menu", on_click=self.drawer.toggle)
                    ui.icon(name="bolt", color=DARK_PINK, size="32px")
                    with ui.link(target=f"/projects/{self.blitz_ui.current_project}"):
                        ui.label("Blitz Dashboard")
                with ItemsCenterContentCenterRow(classes="justify-between"):
                    # with ui.row().classes("items-center justify-between content-center"):
                    with ui.link(target=f"{self.blitz_ui.localhost_url}/projects").classes("disabled"):
                        ui.tooltip("Multiple App management is coming soon")
                        ui.label("Projects")
                    with ui.link(target="/gpt"):
                        ui.label("GPT Builder")
                    with ui.link(target="https://paperz-org.github.io/blitz/", new_tab=True):
                        ui.label("Documentation")
            with ui.row().classes("items-center content-center my-auto"):
                with ui.element():
                    ui.button(
                        icon="dark_mode",
                        on_click=lambda: self.dark_mode.set_value(True),
                    ).props("flat fab-mini color=black disabled").bind_visibility_from(
                        self.dark_mode, "value", value=False
                    )
                    ui.button(
                        icon="light_mode",
                        on_click=lambda: self.dark_mode.set_value(False),
                    ).props("flat fab-mini color=white disabled").bind_visibility_from(
                        self.dark_mode, "value", value=True
                    )
                    ui.tooltip("White mode is coming soon")
                with ui.link(target="https://github.com/Paperz-org/blitz", new_tab=True).classes(" w-8"):
                    ui.image(Path(__file__).parent.parent / "./assets/github_white.png").classes("w-8 ")


class FrameComponent(BaseComponent):
    def __init__(self, show_drawer: bool = True, drawer_open: bool = True) -> None:
        self.show_drawer = show_drawer
        self.drawer_open = drawer_open

        self.drawer: DashboardDrawer | None = None
        super().__init__()

    def render(self) -> None:
        if self.show_drawer and self.blitz_ui.current_project is not None:
            self.drawer = DashboardDrawer(drawer_open=self.drawer_open)
        HeaderComponent(drawer=self.drawer)
