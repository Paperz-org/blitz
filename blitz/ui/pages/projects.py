from nicegui import ui

from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components.buttons.flat import FlatButton
from blitz.ui.components.labels import Label
from blitz.ui.components.tooltip import Tooltip


class ProjectDetail:
    def __init__(
        self,
        app_name: str,
        project_name: str = "",
        date: str = "",
        description: str = "",
        version: str = "",
    ) -> None:
        self.app_name = app_name
        self.project_name = project_name
        self.date = date
        self.description = description
        self.version = version

    def render(self) -> None:
        with ui.link(target=f"/projects/{self.app_name}").classes("w-full hover:bg-slate-700 rounded-sm"), ui.grid(
            columns=20
        ).classes("w-full my-2"):
            Label(self.app_name).ng.classes("col-span-2 pl-2")
            Label(self.project_name).ng.classes("col-span-2 pl-2")
            Label(self.date).ng.classes("col-span-4")
            Label(self.description).ng.classes("col-span-11")
            Label(self.version).ng.classes("col-span-1")


class HomePage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui

    def render_page(self) -> None:
        with ui.element("div").classes("w-full justify-center items-center content-center p-10"):
            with ui.card().classes("no-shadow border align-center"):
                with ui.row().classes("w-full justify-between items-center"):
                    Label("Blitz Projects").ng.classes("text-2xl")
                    with FlatButton("New").props("disabled"):
                        Tooltip("This feature is not developed yet. Create a new project with the CLI.")
                ui.input(label="Search for project").props("borderless standout dense").classes(
                    " rounded-lg px-2 border-solid border w-full my-5"
                )
                with ui.grid(columns=20).classes("w-full"):
                    Label("App").ng.classes("col-span-2 pl-2")
                    Label("Name").ng.classes("col-span-2 pl-2")
                    Label("Last modified").ng.classes("col-span-4")
                    Label("Description").ng.classes("col-span-11")
                    Label("Version").ng.classes("col-span-1")

                ui.separator()

                for app in self.blitz_ui.apps:
                    ProjectDetail(
                        app_name=app.name,
                        project_name=app.file.config.name,
                        description=app.file.config.description or "",
                        version=app.file.config.version,
                    ).render()
