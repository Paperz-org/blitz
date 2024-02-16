from nicegui import ui

from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui

from blitz.ui.components.logger import LogComponent
from blitz.ui.components.status import StatusComponent


class ProjectDetailComponent:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui
        self.app = self.blitz_ui.current_app

    def render(self) -> None:
        with ui.row().classes("w-full justify-between items-center"):
            if self.app is None:
                # TODO handle error
                raise Exception
            ui.label(f"{self.app.file.config.name}").classes("text-xl font-bold")
            ui.label(f"Version: {self.app.file.config.version}").classes("font-bold text-sm")
            ui.separator()
        ui.label(f"Project Path: {self.app.path}").classes("text-sm")
        ui.label(f"Description: {self.app.file.config.description}").classes("text-sm font-normal")


class DashboardPage:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui
        self.app = self.blitz_ui.current_app
        self.columns, self.rows = self.blitz_ui.get_ressources()

    def render_page(self) -> None:
        with ui.element("div").classes("w-full h-full flex flex-row justify-center"):
            with ui.column().classes("w-2/3 h-full border rounded-lg border-gray-300"):
                with ui.expansion("Project", value=True, icon="info").classes("w-full text-bold text-2xl "):
                    ProjectDetailComponent().render()
                with ui.expansion("Models", value=True, icon="help_outline").classes("w-full text-bold text-2xl"):
                    ui.table(columns=self.columns, rows=self.rows, row_key="name").classes("w-full no-shadow")
                with ui.expansion("Status", value=True, icon="health_and_safety").classes("w-full text-bold text-2xl"):
                    # See https://github.com/zauberzeug/nicegui/issues/2174
                    StatusComponent().render()  # type: ignore
                with ui.expansion("Logs", value=False, icon="list").classes("w-full text-bold text-2xl"):
                    LogComponent().render()
