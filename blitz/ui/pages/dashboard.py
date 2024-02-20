from nicegui import ui

from blitz.ui.components.base import BaseComponent

from blitz.ui.components.logger import LogComponent
from blitz.ui.components.status import StatusComponent
from blitz.ui.pages.base import BasePage


class ProjectDetailComponent(BaseComponent):
    def render(self) -> None:
        with ui.row().classes("w-full justify-between items-center"):
            if self.current_app is None:
                # TODO handle error
                raise Exception
            ui.label(f"{self.current_app.file.config.name}").classes("text-xl font-bold")
            ui.label(f"Version: {self.current_app.file.config.version}").classes("font-bold text-sm")
            ui.separator()
        ui.label(f"Project Path: {self.current_app.path}").classes("text-sm")
        ui.label(f"Description: {self.current_app.file.config.description}").classes("text-sm font-normal")


class DashboardPage(BasePage):
    PAGE_NAME = "Dashboard"

    def setup(self) -> None:
        self.columns, self.rows = self.blitz_ui.get_ressources()

    def render(self) -> None:
        with ui.element("div").classes("w-full h-full flex flex-row justify-center"):
            with ui.column().classes("w-2/3 h-full border rounded-lg border-gray-300"):
                with ui.expansion("Project", value=True, icon="info").classes("w-full text-bold text-2xl "):
                    ProjectDetailComponent().render()
                with ui.expansion("Resources", value=True, icon="help_outline").classes("w-full text-bold text-2xl"):
                    ui.table(columns=self.columns, rows=self.rows, row_key="name").classes("w-full no-shadow")
                with ui.expansion("Status", value=True, icon="health_and_safety").classes("w-full text-bold text-2xl"):
                    # See https://github.com/zauberzeug/nicegui/issues/2174
                    StatusComponent().render()  # type: ignore
                with ui.expansion("Logs", value=False, icon="list").classes("w-full text-bold text-2xl"):
                    LogComponent().render()
