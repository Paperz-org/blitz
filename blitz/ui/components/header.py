from pathlib import Path
from typing import Self

from nicegui import ui

from blitz.ui.components import Component
from blitz.ui.components.buttons.icon import IconButton
from blitz.ui.components.drawers.dashboard import DashboardDrawer
from blitz.ui.components.element import Element
from blitz.ui.components.icon import Icon
from blitz.ui.components.image import Image
from blitz.ui.components.labels import Label
from blitz.ui.components.links import Link
from blitz.ui.components.rows import ItemsCenterContentCenterRow
from blitz.ui.components.tooltip import Tooltip

MAIN_PINK = "#cd87ff"
DARK_PINK = "#a72bff"


class HeaderElement(Component[ui.link]):
    def __init__(self, label: str, link: str, new_tab: bool = False) -> None:
        self.label = label
        self.link = link
        self.new_tab = new_tab
        super().__init__()

    def render(self) -> None:
        with Link(target=self.link, new_tab=self.new_tab) as self.ng:
            Label(self.label)

    def disabled(self) -> Self:
        self.ng.classes("disabled")
        # Can't find better implementation to keep ui.link contract
        self.ng._props["href"] = ""
        return self


class HeaderComponent(Component[ui.header], reactive=False):
    ThemeButton = IconButton.variant(props="fab-mini disabled")

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

        # Need to refacto in another way than using components
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

    def dark_mode_button(self) -> None:
        # Can be factorised for sure
        with Element():
            Tooltip("White mode is coming soon")
            self.ThemeButton(
                icon="dark_mode",
                icon_color="black",
                on_click=lambda: self.dark_mode.set_value(not self.dark_mode.value),
            ).ng.bind_visibility_from(self.dark_mode, "value", value=False)
            self.ThemeButton(
                icon="light_mode",
                icon_color="white",
                on_click=lambda: self.dark_mode.set_value(not self.dark_mode.value),
            ).ng.bind_visibility_from(self.dark_mode, "value", value=True)

    def render(self) -> None:
        with ui.header(bordered=True).classes("pl-1 pr-8 justify-between content-center h-16 backdrop-blur-sm"):
            with ItemsCenterContentCenterRow(classes="space-x-20 my-auto mx-2"):
                with ItemsCenterContentCenterRow(classes="space-x-0"):
                    if self.drawer is not None:
                        IconButton(icon="menu", icon_color="white", on_click=self.drawer.toggle)
                    Icon(name="bolt", color="DARK_PINK", size="32px")
                    HeaderElement(label="Blitz Dashboard", link=f"/projects/{self.blitz_ui.current_project}")

                with ItemsCenterContentCenterRow(classes="justify-between"):
                    with HeaderElement(label="Projects", link="/projects").disabled():
                        Tooltip("Multiple App management is coming soon")
                    HeaderElement(label="GPT Builder", link="/gpt")
                    HeaderElement("Documentation", "https://paperz-org.github.io/blitz/", new_tab=True)
            with ItemsCenterContentCenterRow(classes="my-auto"):
                self.dark_mode_button()
                with HeaderElement("", "https://paperz-org.github.io/blitz/", new_tab=True):
                    Image(Path(__file__).parent.parent / "./assets/github_white.png", classes="w-8")


class FrameComponent(Component[None]):
    def __init__(self, show_drawer: bool = True, drawer_open: bool = True) -> None:
        self.show_drawer = show_drawer
        self.drawer_open = drawer_open

        self.drawer: DashboardDrawer | None = None
        super().__init__()

    def render(self) -> None:
        if self.show_drawer and self.blitz_ui.current_project is not None:
            self.drawer = DashboardDrawer(drawer_open=self.drawer_open)
        HeaderComponent(drawer=self.drawer)
