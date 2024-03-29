import json
from typing import Any
from nicegui import ui, app
from pydantic import ValidationError
import yaml
from blitz.models.blitz.file import BlitzFile
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components.buttons import FlatButton
from blitz.ui.components.header import DARK_PINK, MAIN_PINK
from blitz.ui.components import notify
from blitz.ui.components.rows.base import JustifyBetweenRow


class JsonEditorComponent:
    primary_color = DARK_PINK
    highlight_color = MAIN_PINK

    def __init__(
        self,
        content: dict[str, Any],
    ) -> None:
        self.content = content

    def render(self) -> None:
        ui.json_editor({"content": {"json": self.content}, "readOnly": False}).classes(
            "w-full jse-theme-dark rounded-lg"
        ).style(f"--jse-theme-color: {self.primary_color}; --jse-theme-color-highlight: {self.highlight_color}")


class BlitzFileEditorComponent:
    primary_color = DARK_PINK
    highlight_color = MAIN_PINK

    def __init__(
        self,
        content: dict[str, Any],
        mode: str = "text",
        blitz_ui: BlitzUI = get_blitz_ui(),
    ) -> None:
        self.blitz_ui = blitz_ui
        self._original_content = content
        if app.storage.user.get("blitz_file_content") is not None:
            self.content = app.storage.user.get("blitz_file_content", {})
        else:
            self.content = content
        self.mode = mode
        self.read_only = blitz_ui.read_only
        self._editor_read_only = True

    async def get_data(self) -> None:
        raw_content: dict[str, str] = await self.editor.run_editor_method("get")
        try:
            json_content = json.loads(raw_content.get("text", ""))
        except (json.JSONDecodeError, TypeError):
            return
        self.content = json_content
        app.storage.user["blitz_file_content"] = self.content

    def enable_editor(self) -> None:
        self._editor_read_only = not self._editor_read_only
        self.editor.run_editor_method("updateProps", {"readOnly": self._editor_read_only})

    def reset_content(self) -> None:
        self.content = self._original_content
        self.editor.run_editor_method("update", {"json": self.content})
        app.storage.user["blitz_file_content"] = self.content

        notify.success("Content Reset")

    def validate(self) -> None:
        try:
            BlitzFile.from_dict(self.content)
        except ValidationError:
            notify.error("Invalid Blitz File")
        else:
            notify.success("Valid Blitz File")

    def save(self) -> None:
        if self.read_only:
            notify.error("Read Only Mode")
            return
        try:
            BlitzFile.from_dict(self.content)
        except ValidationError:
            notify.error("Invalid Blitz File")
            return
        try:
            if self.blitz_ui.current_app is None:
                # TODO: handle error
                raise Exception
            if self.blitz_ui.current_app.file.path is None:
                # TODO: handle error
                raise Exception
            with open(self.blitz_ui.current_app.file.path, "w") as f:
                if self.blitz_ui.current_app.file.file_type == BlitzFile.FileType.JSON:
                    f.write(json.dumps(self.content, indent=4))
                elif self.blitz_ui.current_app.file.file_type == BlitzFile.FileType.YAML:
                    f.write(yaml.dump(self.content, indent=4))
        except Exception:
            notify.error("Error While Saving File")
        else:
            notify.success("Content Saved")

    def render(self) -> None:
        with ui.row().classes("w-full justify-between align-center p-4 rounded-lg border"):
            with JustifyBetweenRow():
                ui.switch("Edit BlitzFile", on_change=self.enable_editor)
                FlatButton("Reset", on_click=self.reset_content, icon="restart_alt")
            with JustifyBetweenRow():
                FlatButton("Validate", on_click=self.validate, icon="verified")

                FlatButton("Save", on_click=self.save, icon="save")
        self.editor = (
            ui.json_editor(
                {
                    "content": {"json": self.content},
                    "readOnly": self._editor_read_only,
                    "mode": self.mode,
                },
                on_change=self.get_data,
            )
            .classes("w-full jse-theme-dark rounded-lg")
            .style(f"--jse-theme-color: {self.primary_color}; --jse-theme-color-highlight: {self.highlight_color}")
        )
