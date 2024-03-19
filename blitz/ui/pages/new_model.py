from blitz.models.blitz.field import AllowedBlitzFieldTypes
from blitz.ui.components.buttons.flat import FlatButton
from blitz.ui.components.icon.base import BaseIcon
from blitz.ui.components.labels.base import BaseLabel as Label
from blitz.ui.components.rows.base import BaseRow, WFullItemsCenterRow, WFullRow, WFullSpaceBetweenRow
from blitz.ui.pages.base import BasePage
from nicegui import ui


class NewModelPage(BasePage):

    def get_allowed_blitz_type(self) -> dict[str, str]:
        return {str(value): value.capitalize().replace("_", " ") for value in AllowedBlitzFieldTypes}
    
    def render(self) -> None:
        with ui.card().classes("no-shadow w-full"):
            with WFullSpaceBetweenRow():
                Label("Resource", classes="text-2xl")
                with BaseRow():
                    FlatButton("Edit")
                    FlatButton("Save")
        
            
            ui.input("Name").props("borderless standout dense").classes("grow rounded-lg px-2 border-solid border")
                
        with ui.card().classes("no-shadow w-full"):
            with WFullSpaceBetweenRow():
                Label("Fields")
                FlatButton("New")
            with WFullItemsCenterRow():
                ui.input("Name").props("borderless standout dense").classes("grow rounded-lg px-2 border-solid border")
                ui.select(
                    self.get_allowed_blitz_type(),
                    label="Type",
                    value="str",
                ).props("borderless standout dense").classes("w-32 rounded-lg px-2 border-solid border")
                is_nullable = ui.checkbox("Nullable")
                is_unique = ui.checkbox("Unique")
                FlatButton(icon="edit")
                FlatButton(icon="save")
