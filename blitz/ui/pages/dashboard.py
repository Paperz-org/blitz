from nicegui import ui
from blitz.ui.components.accordion.base import BaseAccordion

from blitz.ui.components.base import BaseComponent

from blitz.ui.components.logger import LogComponent
from blitz.ui.components.status import StatusComponent
from blitz.ui.pages.base import BasePage
from blitz.ui.components.labels.base import TextXlLabel, TextSmLabel


class ProjectDetailComponent(BaseComponent[ui.row]):
    TitleLabel = TextXlLabel.variant(classes="font-bold")
    TextLabel = TextSmLabel.variant(classes="font-normal")
    BoldTextLabel = TextSmLabel.variant(classes="font-bold")

    def render(self) -> None:
        with ui.row().classes("w-full justify-between items-center"):
            if self.current_app is None:
                # TODO handle error
                raise Exception
            self.TitleLabel(f"{self.current_app.file.config.name}")
            self.BoldTextLabel(f"Version: {self.current_app.file.config.version}")
            ui.separator()
        self.BoldTextLabel(f"Project Path: {self.current_app.path}")
        self.TextLabel(f"Description: {self.current_app.file.config.description}")


class DashboardPage(BasePage):
    PAGE_NAME = "Dashboard"
    Accordion = BaseAccordion.variant(classes="w-full text-bold text-2xl")

    def setup(self) -> None:
        self.columns, self.rows = self.blitz_ui.get_ressources()

    def render(self) -> None:
        with ui.element("div").classes("w-full h-full flex flex-row justify-center") as self.ng:
            with ui.column().classes("w-2/3 h-full border rounded-lg border-gray-300"):
                with self.Accordion("Project", icon="info", is_open=True):
                    ProjectDetailComponent()
                with self.Accordion("Resources", icon="help_outline", is_open=True):
                    ui.table(columns=self.columns, rows=self.rows, row_key="name").classes("w-full no-shadow")
                with self.Accordion("Status", icon="health_and_safety", is_open=True):
                    StatusComponent()
                with self.Accordion("Logs", icon="list", is_open=False):
                    LogComponent()
