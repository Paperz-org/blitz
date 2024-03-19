from blitz.ui.blitz_ui import get_blitz_ui
from blitz.ui.components.accordion.base import BaseAccordion
from blitz.ui.components.buttons.flat import FlatButton
from blitz.ui.components.labels.base import Text2XlBoldLabel, TextSmLabel, TextXsLabel
from blitz.ui.components.rows.base import WFullRow
from blitz.ui.pages.base import BasePage
from nicegui import ui

from blitz.ui.components.labels import Label


class ResourcePage(BasePage):
    Accordion = BaseAccordion.variant(classes="w-full text-bold text-2xl")

    def setup(self) -> None:
        self.columns, self.rows = self.blitz_ui.get_ressources()

    @staticmethod
    def _opened(index: int) -> bool:
        return index == 0

    def render(self) -> None:
        self.setup()
        self.blitz_ui = get_blitz_ui()
        with WFullRow():
            Text2XlBoldLabel("Resources")
            FlatButton("New")
        with ui.column().classes("w-2/3"):
            for i, ressource in enumerate(self.blitz_ui.current_app.resources):
                with self.Accordion(
                    ressource.config.name, caption=ressource.config.settings.allowed_methods, is_open=self._opened(i), classes="border rounded-lg border-gray-600"
                ):
                    FlatButton("Edit", icon="edit")
                    with ui.grid(columns=8).classes("w-full"):
                        TextSmLabel("Name", classes="col-span-2")
                        TextSmLabel("Type", classes="col-span-4")
                        TextSmLabel("Unique", classes="col-span-1")
                        TextSmLabel("Nullable", classes="col-span-1")
                    ui.separator()
                    for field_name, config in ressource.config.fields.items():
                        with ui.grid(columns=8).classes("w-full"):
                            TextSmLabel(field_name, classes="col-span-2")
                            if config.type.type.value == "relationship":
                                TextSmLabel(f"{config.type.type.value} -> {config.relationship}", classes="col-span-4")
                            elif isinstance(config.foreign_key, str):
                                TextSmLabel(f"FK {config.type.type.value} -> {config.foreign_key}", classes="col-span-4")
                            else:
                                TextSmLabel(config.type.type.value, classes="col-span-4")
                            
                                
                            TextSmLabel(f"{'Yes' if config.unique else 'No'}", classes="col-span-1")
                            TextSmLabel(f"{'Yes' if config.nullable else 'No'}", classes="col-span-1")
