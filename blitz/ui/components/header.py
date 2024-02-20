from pathlib import Path

from nicegui import ui
from nicegui.page_layout import LeftDrawer
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components.buttons import FlatButton

MAIN_PINK = "#cd87ff"
DARK_PINK = "#a72bff"


class HeaderMenuComponent:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        pass

    def render(self) -> None:
        FlatButton(icon="menu")


class HeaderComponent:
    def __init__(self, title: str = "", blitz_ui: BlitzUI = get_blitz_ui(), drawer: LeftDrawer | None = None) -> None:
        self.title = title
        self.blitz_ui = blitz_ui

        self.dark_mode = ui.dark_mode(value=True)
        self.home_link = f"dashboard/projects/{blitz_ui.current_project}" if blitz_ui.current_project else "projects"
        self.drawer = drawer
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

    def render(self) -> None:
        with ui.header(bordered=True).classes("pl-1 pr-8 justify-between content-center h-16 backdrop-blur-sm"):
            with ui.row().classes("items-center space-x-20 content-center my-auto"):
                with ui.row().classes("items-center space-x-0 content-center "):
                    if self.drawer is not None:
                        FlatButton(icon="menu", on_click=self.drawer.toggle)
                    ui.icon(name="bolt", color=DARK_PINK, size="32px")
                    with ui.link(target=f"/projects/{self.blitz_ui.current_project}"):
                        ui.label("Blitz Dashboard")

                with ui.row().classes("items-center justify-between content-center"):
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


class MenuLink:
    def __init__(self, label: str, link: str, icon: str) -> None:
        self.label = label
        self.link = link
        self.icon = icon

    def render(self) -> None:
        with ui.link(target=self.link).classes("w-full"), ui.button(on_click=self.go_to).props(
            "flat align=left"
        ).classes("px-4 hover:bg-slate-700 rounded-sm w-full") as self.button:
            ui.icon(name=self.icon, size="sm").props("flat").classes("pr-4")
            ui.label(self.label)

    def go_to(self) -> None:
        ui.open(self.link)


class FrameComponent:
    def __init__(
        self,
        blitz_ui: BlitzUI = get_blitz_ui(),
        show_drawer: bool = True,
        drawer_open: bool = True,
    ) -> None:
        self.blitz_ui = blitz_ui
        self.current_project = blitz_ui.current_project
        self.show_drawer = show_drawer
        self.drawer_open = drawer_open

        # Only for declarative
        self.drawer: LeftDrawer | None = None

    def left_drawer(self) -> None:
        with ui.left_drawer(value=self.drawer_open, fixed=True, bottom_corner=True).props("width=200").classes(
            "px-0 bg-[#14151a]"
        ) as self.drawer:
            MenuLink("Dashboard", f"/projects/{self.current_project}", "dashboard").render()
            MenuLink(
                "Admin",
                f"{self.blitz_ui.localhost_url}/admin/",
                "table_chart",
            ).render()
            MenuLink("Swagger", f"/projects/{self.current_project}/swagger", "api").render()
            MenuLink(
                "Blitz File",
                f"/projects/{self.current_project}/blitz-file",
                "article",
            ).render()
            MenuLink(
                "Diagram",
                f"/projects/{self.current_project}/diagram",
                "account_tree",
            ).render()
            MenuLink("Logs", f"/projects/{self.current_project}/logs", "list").render()

    def render(self) -> None:
        if self.show_drawer and self.current_project is not None:
            self.left_drawer()
        HeaderComponent(drawer=self.drawer).render()
