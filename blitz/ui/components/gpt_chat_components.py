import json
import re
from typing import Any, cast
from nicegui import ui
from nicegui.elements.dialog import Dialog
from nicegui.elements.expansion import Expansion
from pydantic import ValidationError
from blitz.models.blitz.file import BlitzFile
from openai.types.chat import ChatCompletionMessageParam
from blitz.ui.components.buttons import FlatButton

import yaml

from blitz.ui.components.buttons.icon import IconButton


class ResponseJSON:
    def __init__(self, text: str) -> None:
        self.text = text
        self.json = self.extract_json(text)

        self.is_valid_blitz_file = self.validate_blitz_file(self.json)

        self.blitz_app_title = self._get_expansion_title(self.json)
        self.color = self._get_color(self.is_valid_blitz_file)

        self._expansion: Expansion | None = None
        self._expansion_is_open = self.is_valid_blitz_file
        self._dialog: Dialog | None = None

    @staticmethod
    def _get_expansion_title(blitz_file: dict[str, dict[str, Any]]) -> str:
        name_part = blitz_file.get("config", {}).get("name", "Blitz App")
        version = blitz_file.get("config", {}).get("version", "0.0.0")
        return f"{name_part} v{version}"

    @staticmethod
    def _get_color(is_valid: bool) -> str:
        if is_valid:
            return "text-green"
        return "text-red"

    def validate_blitz_file(self, json: dict[str, Any]) -> bool:
        try:
            BlitzFile.from_dict(json)
        except ValidationError:
            return False
        except Exception:
            return False
        else:
            return True

    @staticmethod
    def extract_json(text: str) -> Any:
        json_pattern = r"```json([\s\S]*?)```"
        match = re.search(json_pattern, text)
        if match is None:
            # TODO: handle error
            raise Exception
        return json.loads(match.group(1))

    async def copy_code(self) -> None:
        ui.run_javascript(f"navigator.clipboard.writeText(`{json.dumps(self.json, indent=4)}`)")
        ui.notify("Copied to clipboard", type="info", color="green")

    def action_buttons(self) -> None:
        with ui.row(wrap=False).classes("items-center"):
            if self._dialog is None:
                # TODO: handle error
                raise Exception
            IconButton(icon="content_copy", icon_color="grey", on_click=self.copy_code)
            IconButton(icon="file_download", icon_color="grey", on_click=self._dialog.open)

    def download_dialog(self) -> None:
        with ui.dialog() as self._dialog, ui.card().classes("w-full px-4"):
            if self.is_valid_blitz_file is False:
                self.invalid_blitz_file()
            # with ui.expansion("Edit File", icon="edit").classes("w-full h-auto rounded-lg border-solid border overflow-hidden grow overflow-hidden"):
            #    JsonEditorComponent(self.json).render()
            with ui.row().classes("w-full justify-end"):
                FlatButton("Export as JSON", on_click=self._download_json)
                FlatButton("Export as YAML", on_click=self._download_yaml)

    def _download_json(self) -> None:
        ui.download(
            str.encode(json.dumps(self.json, indent=4)),
            filename=self._get_filename("json"),
        )

    def _download_yaml(self) -> None:
        ui.download(str.encode(yaml.dump(self.json)), filename=self._get_filename("yaml"))

    def _get_filename(self, extension: str) -> str:
        return f"{self.blitz_app_title.replace(' ', '_').replace('.', '_').lower()}.{extension}"

    def invalid_blitz_file(self) -> None:
        with ui.row().classes("items-center"):
            ui.icon("error", color="red", size="sm")
            ui.label("This is not a valid Blitz file.").classes("text-red")

    def _toggle_expansion(self) -> None:
        self._expansion_is_open = not self._expansion_is_open
        if self._expansion is None:
            # TODO: handle error
            raise Exception
        self._expansion.value = self._expansion_is_open

    @ui.refreshable
    def render(self) -> None:
        self.download_dialog()
        with ui.row(wrap=False).classes("items-center w-full"):
            with ui.expansion(
                self.blitz_app_title,
                icon="settings_suggest",
                value=self._expansion_is_open,
                on_value_change=self._toggle_expansion,
            ).classes("rounded-lg border-solid border overflow-hidden grow").props(
                f"overflow-hidden header-class={self.color}"
            ) as self._expansion:
                if not self.is_valid_blitz_file:
                    self.invalid_blitz_file()
                ui.markdown(self.text)
            self.action_buttons()


class MarkdownResponse:
    def __init__(self, text: str) -> None:
        self.text = text

    @ui.refreshable
    def render(self) -> None:
        ui.markdown(self.text)


class GPTChatComponent:
    def __init__(
        self,
        label: str,
        icon: str,
        text: str,
        avatar_color: str | None = None,
    ) -> None:
        self.response_json = None
        self.label = label
        self.text = text
        self.icon = icon
        self.avatar_color = avatar_color
        self.text_components: list[Any] = []

    @ui.refreshable
    def render(self) -> None:
        with ui.row(wrap=False).classes("w-full"):
            ui.space().classes("w-1/3")
            with ui.column().classes("justify-start w-2/3"):
                with ui.row(wrap=False).classes("items-center w-full"):
                    with ui.avatar(color=self.avatar_color).props("size=sm"):
                        ui.icon(self.icon, size="xs", color="white")
                    ui.label(self.label).classes("font-bold")

                if self.text_components:
                    for component in self.text_components:
                        with ui.element().classes("px-10 w-full"):
                            component.render()
                else:
                    with ui.element().classes("px-10"):
                        ui.markdown(self.text)
            ui.space().classes("w-1/3")

    def as_gpt_dict(self) -> ChatCompletionMessageParam:
        raise NotImplementedError

    def to_dict(self) -> dict[str, Any]:
        raise NotImplementedError


class UserQuestion(GPTChatComponent):
    LABEL = "You"
    ICON = "person"
    AVATAR_COLOR = "#a72bff"

    def __init__(self, text: str = "") -> None:
        super().__init__(label=self.LABEL, text=text, icon=self.ICON, avatar_color=self.AVATAR_COLOR)

    def as_gpt_dict(self) -> ChatCompletionMessageParam:
        return {
            "content": self.text,
            "role": "user",
            "name": "user",
        }

    def to_dict(self) -> dict[str, Any]:
        return cast(dict[str, Any], self.as_gpt_dict())

    @classmethod
    def from_gpt_dict(cls, gpt_dict: dict[str, str]) -> "UserQuestion":
        return cls(text=gpt_dict.get("content", ""))


class GPTResponse(GPTChatComponent):
    LABEL = "GPT"
    ICON = "self_improvement"
    AVATAR_COLOR = "#74aa9c"

    def __init__(self, text: str = "", text_is_finished: bool = False) -> None:
        super().__init__(label=self.LABEL, text=text, icon=self.ICON, avatar_color=self.AVATAR_COLOR)
        self._text_is_finished: bool
        self.text_is_finished = text_is_finished

    def add(self, text: str) -> None:
        self.text += text
        self.render.refresh()

    @property
    def text_is_finished(self) -> bool:
        return self._text_is_finished

    @text_is_finished.setter
    def text_is_finished(self, value: bool) -> None:
        if value is True:
            self._text_is_finished = value
            self.text_components = self.split_response(self.text)
            self.render.refresh()
        else:
            self._text_is_finished = value

    def as_gpt_dict(self) -> ChatCompletionMessageParam:
        return {
            "content": self.text,
            "role": "system",
            "name": "Blitz",
        }

    def to_dict(self) -> dict[str, Any]:
        dict_ = cast(dict[str, Any], self.as_gpt_dict())
        dict_["text_is_finished"] = self.text_is_finished
        return dict_

    @staticmethod
    def split_response(text: str) -> list[Any]:
        json_pattern = r"(```json[\s\S]*?```)"

        # Search for JSON content in the Markdown text
        components: list[ResponseJSON | MarkdownResponse] = []
        for match in re.split(json_pattern, text):
            if re.match(json_pattern, match):
                components.append(ResponseJSON(match))
            else:
                components.append(MarkdownResponse(match))
        return components

    @classmethod
    def from_gpt_dict(cls, gpt_dict: dict[str, Any]) -> "GPTChatComponent":
        return cls(
            text=gpt_dict.get("content", ""),
            text_is_finished=gpt_dict.get("text_is_finished", False),
        )
