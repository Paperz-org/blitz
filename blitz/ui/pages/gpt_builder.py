from functools import lru_cache
from typing import Any, AsyncGenerator, Callable, cast
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from nicegui import ui, app
from nicegui.events import KeyEventArguments
from openai import APIConnectionError, AsyncOpenAI, AsyncStream, AuthenticationError

from blitz.settings import get_settings
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from blitz.ui.components import notify
from blitz.ui.components.buttons.flat import FlatButton
from blitz.ui.components.buttons.icon import IconButton
from blitz.ui.components.buttons.outline import OutlineButton
from blitz.ui.components.gpt_chat_components import (
    GPTChatComponent,
    GPTResponse,
    UserQuestion,
)
from blitz.ui.components.header import FrameComponent
from blitz.ui.components.labels.base import BoldLabel, Text2XlBoldLabel, TextXlBoldLabel, TextXsLabel
from blitz.ui.components.rows.base import WFullItemsCenterRow
from blitz.ui.pages.base import BasePage
from blitz.ui.components.labels import Label

DEV_TEXT = """Sure! Here is a sample blitz_file with randomly generated models and fields:

```json
{
  "config": {
    "name": "Random App",
    "description": "A randomly generated Blitz app",
    "version": "1.0.0"
  },
  "resources": [
    {
      "name": "User",
      "fields": {
        "name": "str",
        "age": "int",
        "email": "str",
        "address": "str"
      }
    },
    {
      "name": "Product",
      "fields": {
        "name": "str",
        "description": "str",
        "price": "float",
        "quantity": "int"
      }
    },
    {
      "name": "Order",
      "fields": {
        "user_id": "User.id",
        "product_id": "Product.id",
        "quantity": "int",
        "total_price": "float"
      }
    }
  ]
}
```

Please note that this blitz_file is randomly generated and may not have any specific meaning or logic."""


class GPTClient:
    CloseButton = IconButton.variant(icon="close")

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", pre_prompt: str | None = None) -> None:
        self.model = model
        self._api_key = api_key
        self.pre_prompt = pre_prompt
        self.client = self._get_client(api_key=api_key) if api_key else None

    @staticmethod
    def _get_client(api_key: str) -> AsyncOpenAI:
        return AsyncOpenAI(api_key=api_key)

    def _add_preprompt(self, messages: list[ChatCompletionMessageParam]) -> list[ChatCompletionMessageParam]:
        messages.insert(
            0,
            {
                "content": self.pre_prompt or "",
                "role": "system",
                "name": "BlitzUI",
            },
        )
        return messages

    def refresh_client(self, api_key: str) -> None:
        self._api_key = api_key
        self.client = self._get_client(api_key=api_key)

    async def stream(self, messages: list[ChatCompletionMessageParam]) -> AsyncStream[ChatCompletion]:
        if self.pre_prompt:
            messages = self._add_preprompt(messages)
        if self.client is None:
            # TODO: handle this error
            raise Exception
        return cast(
            AsyncStream[ChatCompletion],
            await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
            ),
        )

    async def list_models(self) -> Any:
        if self.client is None:
            # TODO: handle this error
            raise Exception
        return await self.client.models.list()


@lru_cache
def get_gpt_client() -> GPTClient:
    return GPTClient(api_key=get_settings().BLITZ_OPENAI_API_KEY)


class AskGPTPage(BasePage):
    PAGE_NAME = "GPT Builder"
    FRAME = FrameComponent(show_drawer=False)

    def setup(self, gpt_client: GPTClient = get_gpt_client()) -> None:
        self.gpt_client = gpt_client
        self.gpt_client.pre_prompt = self.blitz_ui.preprompt
        self._gpt_client_error = False
        self.gpt_request: str = ""
        self.gpt_messages: list[GPTChatComponent] = []

        if messages := app.storage.user.get("gpt_messages", []):
            self.gpt_messages = [
                (
                    UserQuestion.from_gpt_dict(message)
                    if message["role"] == "user"
                    else GPTResponse.from_gpt_dict(message)
                )
                for message in messages
            ]

        # Theses variables are the result of `ui.state(False)` defined in the chat_area method
        # because it need to be in a ui.refreshable component
        self.thinking: bool
        self.set_thinking: Callable[[bool], None]

        # Here because otherwise when the ui refresh the scroll is reset to top (???)
        self._scroll_area = ui.scroll_area().classes("flex-grow")

        # Only declarative
        self.settings_dialog: ChatSettings | None = None

    @property
    def can_send_request(self) -> bool:
        return self.gpt_request != "" or self.thinking is True

    @property
    def gpt_client_is_valid(self) -> bool:
        return self.gpt_client.client is not None and self._gpt_client_error is False

    @property
    def gpt_client_error(self) -> bool:
        return self._gpt_client_error

    def render(self) -> None:
        # Allow the full size of the scrollable zone
        ui.query(".q-page").classes("flex")
        ui.query(".nicegui-content").classes("w-full")

        # Allow the usage of cmd + enter to send the request
        ui.keyboard(on_key=self.handle_key, ignore=[])

        self.settings_dialog = ChatSettings(self.gpt_client)
        # See https://github.com/zauberzeug/nicegui/issues/2174
        self.settings_dialog.render()  # type: ignore
        self.delete_conversation()

        # All the components of the chat
        # See https://github.com/zauberzeug/nicegui/issues/2174
        self.chat_area()  # type: ignore

        # The footer with the input and the send button
        self.footer()
        FrameComponent(show_drawer=False).render()

    def footer(self) -> None:
        with ui.footer().classes("items-center space-y-0 pt-0 justify-center px-5"):
            with ui.grid(columns=10).classes("w-full items-center gap-5"):
                IconButton(
                    icon="delete_outline",
                    icon_color="grey-8",
                    icon_size="lg",
                    on_click=self.delete_conversation_dialog.open,
                    classes="justify-self-start",
                )
                IconButton(
                    icon="settings",
                    icon_color="grey-6",
                    icon_size="lg",
                    on_click=self.open_settings,
                    classes="justify-self-end",
                )
                with ui.row(wrap=False).classes(
                    "w-full items-center rounded-lg pl-2 border-solid border col-start-3 col-span-6"
                ):
                    ui.textarea(on_change=lambda: self.ask_button.refresh()).props(
                        "borderless autogrow standout clearable dense"
                    ).classes("flex-grow w-auto ").bind_value(self, "gpt_request")
                    # See https://github.com/zauberzeug/nicegui/issues/2174
                    self.ask_button()  # type: ignore
                ui.space().classes("col-span-2")

            TextXsLabel(
                "ChatGPT can make mistakes. Consider checking important information.",
                classes="text-gray-500 w-full text-center",
            )

    def delete_conversation(self) -> None:
        with ui.dialog() as self.delete_conversation_dialog, ui.card().classes("no-shadow"):
            Label("Are you sure you want to delete this conversation?")
            with ui.row().classes("w-full items-center"):
                FlatButton("Cancel", on_click=self.delete_conversation_dialog.close)
                FlatButton("Delete", on_click=self._handle_delete_conversation)

    def _handle_delete_conversation(self) -> None:
        self.remove_conversation()
        self.delete_conversation_dialog.close()

    def open_settings(self) -> None:
        if self.settings_dialog is None:
            # TODO: handle error
            raise Exception
        self.settings_dialog.refresh()
        self.settings_dialog.open()

    def remove_conversation(self) -> None:
        self.gpt_messages = []
        app.storage.user["gpt_messages"] = []
        self.chat_area.refresh()

    @ui.refreshable
    def chat_area(self) -> None:
        self.thinking, self.set_thinking = ui.state(False)

        # Here because otherwise when the ui refresh the scroll is reset to top (???)
        # Same as comment in __init__, we need to clean the scroll_area otherwise all the message are duplicated
        self._scroll_area.clear()

        with self._scroll_area:
            for message in self.gpt_messages:
                # See https://github.com/zauberzeug/nicegui/issues/2174
                message.render()  # type: ignore

    @ui.refreshable
    def ask_button(self) -> None:
        IconButton(
            icon="send" if not self.thinking else "stop_circle",
            icon_color="purple-4",
            on_click=self.ask_button_trigger,
            props="fab-mini",
        ).ng.bind_enabled_from(self, "can_send_request")

    async def handle_key(self, e: KeyEventArguments) -> None:
        if e.modifiers.meta and e.key.enter and self.can_send_request:
            await self.ask_button_trigger()

    async def ask_button_trigger(self) -> None:
        self.set_thinking(not self.thinking)
        if self.thinking:
            self.gpt_messages.append(UserQuestion(self.gpt_request))
            self.chat_area.refresh()
            try:
                await self._handle_ask_event()
            except AuthenticationError:
                self._gpt_client_error = True

            self.set_thinking(False)
        else:
            self.gpt_request = ""

        app.storage.user["gpt_messages"] = [message.to_dict() for message in self.gpt_messages]
        self.ask_button.refresh()

    async def _handle_ask_event(self) -> None:
        gpt_response = GPTResponse()
        self.gpt_messages.append(gpt_response)

        self.chat_area.refresh()
        self.gpt_request = ""

        async for i in self.ask_gpt():
            gpt_response.add(i)
            self._scroll_area.scroll_to(percent=100)
        gpt_response.text_is_finished = True

    async def ask_gpt(self) -> AsyncGenerator[str, None]:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "name": "BlitzUI",
                "content": self.blitz_ui.preprompt,
            }
        ]
        messages.extend([message.as_gpt_dict() for message in self.gpt_messages])

        stream = await self.gpt_client.stream(messages=messages)

        async for chunk in stream:
            if self.thinking is False:
                break
            # TODO: wtf, delta doesn't exists in the openai types Choice but this is working
            if chunk.choices[0].delta.content is not None:  # type: ignore
                yield chunk.choices[0].delta.content  # type: ignore


class ChatSettings:
    def __init__(
        self,
        gpt_client: GPTClient,
        blitz_ui: BlitzUI = get_blitz_ui(),
    ) -> None:
        self.gpt_client = gpt_client
        self.dialog = ui.dialog().props("maximized transition-show=slide-up transition-hide=slide-down")
        self.blitz_ui = blitz_ui
        self.quit_dialog = ui.dialog(value=False)

    @ui.refreshable
    def render(self) -> None:
        """Render the settings dialog"""
        with self.dialog, ui.card().classes("w-full px-4"):
            self.quit_modal()
            self.header()
            TextXlBoldLabel("OpenAI")
            # See https://github.com/zauberzeug/nicegui/issues/2174
            self.openai_settings()  # type: ignore
            TextXlBoldLabel("Pre Prompt")
            # See https://github.com/zauberzeug/nicegui/issues/2174
            self.pre_prompt_editor()  # type: ignore

    def api_key_input_component(self) -> None:
        """Create the api key input component"""
        self.api_key_input = (
            ui.input(
                "OpenAI API Key",
                value=self.gpt_client._api_key,
                placeholder="sk-...",
                password=True,
                password_toggle_button=True,
            )
            .props("borderless standout dense")
            .classes("grow rounded-lg px-2 border-solid border")
        )

    def header(self) -> None:
        """Render the header of the settings dialog"""
        with WFullItemsCenterRow(classes="justify-center"):
            IconButton(icon="close", icon_color="white", on_click=self.close)
            Text2XlBoldLabel("Chat Settings", classes="grow text-center")
            FlatButton("Save", icon="save", on_click=self.save, classes="text-color-black").ng.bind_enabled_from(
                self, "settings_has_changed"
            )

    @ui.refreshable
    def openai_settings(self) -> None:
        """Render the openai settings"""
        with WFullItemsCenterRow():
            self.model_select = (
                ui.select(
                    {"gpt-3.5-turbo": "3.5 Turbo", "gpt-4": "4"},
                    label="Model",
                    value=self.gpt_client.model,
                )
                .props("borderless standout dense")
                .classes("w-32 rounded-lg px-2 border-solid border")
            )
            self.api_key_input_component()
            OutlineButton("Check API KEY", on_click=self.validate_api_key)
            ui.space()

    @ui.refreshable
    def pre_prompt_editor(self) -> None:
        with WFullItemsCenterRow():
            OutlineButton("Reset Pre-Prompt", on_click=self.reset_preprompt)
            switch = ui.switch("Edit Pre-Prompt", value=False)
        self.preprompt = (
            ui.textarea(label="Pre-Prompt", value=self.blitz_ui.preprompt)
            .classes("w-full rounded-lg px-2 border-solid border")
            .props("borderless autogrow")
            .bind_enabled_from(switch, "value")
        )

    def open(self) -> None:
        self.dialog.open()

    @property
    def settings_has_changed(self) -> bool:
        if self.gpt_client.model != self.model_select.value:
            return True
        if self.blitz_ui.preprompt != self.preprompt.value:
            return True
        if self.gpt_client._api_key != self.api_key_input.value:
            return True
        return False

    def refresh(self) -> None:
        self.openai_settings.refresh()
        self.pre_prompt_editor.refresh()

    def reset_preprompt(self) -> None:
        self.blitz_ui.reset_preprompt()
        self.pre_prompt_editor.refresh()

    def quit_modal(self) -> None:
        with self.quit_dialog, ui.card():
            with WFullItemsCenterRow():
                IconButton(icon="close", on_click=self.quit_dialog.close)
                BoldLabel("Some changes wasn't saved.")
            with WFullItemsCenterRow():
                FlatButton("Discard changes", on_click=self.quit)
                FlatButton("Save", on_click=self.save)

    def close(self) -> None:
        if self.settings_has_changed:
            self.quit_dialog.open()
        else:
            self.quit()

    def quit(self) -> None:
        if self.quit_dialog.value:
            self.quit_dialog.close()
        self.dialog.close()

    def save(self) -> None:
        if self.quit_dialog.value:
            self.quit_dialog.close()

        self.gpt_client.model = self.model_select.value
        self.blitz_ui.preprompt = self.preprompt.value
        self.gpt_client.refresh_client(api_key=self.api_key_input.value)
        notify.success("Settings saved")
        self.dialog.close()

    async def validate_api_key(self) -> None:
        try:
            gpt_client = GPTClient(api_key=self.api_key_input.value)
            await gpt_client.list_models()
            notify.success("Valid API Key")
        except (AuthenticationError, APIConnectionError):
            notify.warning("Invalid API Key")
