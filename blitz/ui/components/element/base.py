from nicegui import Client, ui

from blitz.ui.components.base import BaseComponent


class BaseElement(BaseComponent[ui.element]):
    def __init__(
        self, tag: str | None = None, _client: Client | None = None, props: str = "", classes: str = ""
    ) -> None:
        self.tag = tag
        self._client = _client
        super().__init__(props=props, classes=classes)

    def render(self) -> None:
        self.ng = ui.element(tag=self.tag, _client=self._client).props(self.props).classes(self.classes)


class IFrame(BaseElement):  # type: ignore
    """
    IFrame element.

    args:
        src: str - URL to load in the iframe.
        frameborder: int - Frame border width.
    """

    def __init__(self, src: str, frameborder: int, props: str = "", classes: str = "") -> None:
        props = f"src={src} frameborder={frameborder} {props}"
        super().__init__("iframe", props=props, classes=classes)
