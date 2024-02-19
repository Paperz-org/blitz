import logging
from typing import TYPE_CHECKING
from blitz.ui.blitz_ui import get_blitz_ui
from blitz.ui.pages import (
    BlitzFilePage,
    DashboardPage,
    MermaidPage,
    AskGPTPage,
    LogPage,
    SwaggerPage,
)
from pathlib import Path
from blitz.ui.router import BlitzRouter
from nicegui import ui

if TYPE_CHECKING:
    from blitz.api.blitz_api import BlitzAPI


def init_routers() -> None:
    router = BlitzRouter("/")
    router.add_page("gpt", AskGPTPage)

    project_router = BlitzRouter("/projects/{uuid}/")
    project_router.add_page("logs", LogPage)
    project_router.add_page("swagger", SwaggerPage)
    project_router.add_page("blitz-file", BlitzFilePage)
    project_router.add_page("diagram", MermaidPage)
    project_router.add_page("", DashboardPage)


# @ui.page("/projects")
# def projects_page(blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
# ui.page_title("Projects")
# HomePage().render_page()
# FrameComponent(show_drawer=False).render()


def init_ui(
    blitz_api: "BlitzAPI",
    mount_path: str = "/dashboard",
    storage_secret: str = "secret",
    title: str = "Dashboard",
) -> None:
    logging.getLogger("niceGUI").setLevel(logging.WARNING)
    blitz_ui = get_blitz_ui()
    blitz_ui.current_app = blitz_api.blitz_app
    print("________", blitz_ui)
    init_routers()
    ui.run_with(
        app=blitz_api,
        title=title,
        dark=True,
        mount_path=mount_path,
        storage_secret=storage_secret,
        favicon=Path(__file__).parent / "./assets/favicon.ico",
    )
