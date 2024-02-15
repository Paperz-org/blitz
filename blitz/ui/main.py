import logging
from typing import TYPE_CHECKING, Annotated

from blitz.app import BlitzApp
from blitz.core import BlitzCore
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.pages.admin import AdminPage
from blitz.ui.pages.blitz_file import BlitzFilePage
from blitz.ui.pages.dashboard import DashboardPage
from blitz.ui.pages.diagram import MermaidPage
from blitz.ui.pages.gpt_builder import AskGPTPage
from blitz.ui.pages.log import LogPage
from blitz.ui.pages.projects import HomePage
from blitz.ui.pages.swagger import SwaggerPage
from pathlib import Path
from nicegui import ui

from nicegui import ui
from pydantic import BaseModel
from nicegui import app, ui

from blitz.ui.components.header import FrameComponent, HeaderComponent


from fastapi import Depends, FastAPI, Request

from nicegui import app, ui

if TYPE_CHECKING:
    from blitz.api.blitz_api import BlitzAPI


async def _post_dark_mode(request: Request) -> None:
    print("dark mode")
    app.storage.browser["dark_mode"] = (await request.json()).get("value")


@ui.page("/projects/{uuid}", title="Dashboard")
def dashboard_page(uuid: str, blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
    DashboardPage().render_page()
    FrameComponent().render()


@ui.page("/projects/{uuid}/diagram", title="Diagram")
def diagram_page(uuid: str, blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
    MermaidPage().render_page()
    FrameComponent().render()


@ui.page("/projects/{uuid}/blitz-file", title="Blitz File")
def blitz_file_page(uuid: str, blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
    BlitzFilePage().render_page()
    FrameComponent().render()


@ui.page("/projects/{uuid}/swagger", title="Swagger")
def swagger_page(uuid: str, blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
    SwaggerPage().render_page()
    FrameComponent().render()


@ui.page("/projects/{uuid}/logs")
def log_page(uuid: str, blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
    ui.page_title("Logs")
    LogPage().render_page()
    FrameComponent().render()


# @ui.page("/projects/{uuid}/admin")
# def log_page(uuid: str, blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
#     ui.page_title("Admin")
#     AdminPage().render_page()
#     FrameComponent(drawer_open=False).render()


@ui.page("/gpt")
def ask_gpt_page(blitz_ui: Annotated[BlitzUI, Depends(get_blitz_ui)]) -> None:
    ui.page_title("GPT Builder")
    AskGPTPage().render_page()
    FrameComponent(show_drawer=False).render()


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
    ui.run_with(
        app=blitz_api,
        title=title,
        dark=True,
        mount_path=mount_path,
        storage_secret=storage_secret,
        favicon=Path("blitz/ui/assets/favicon.ico"),
    )
