from typing import Type
from nicegui import ui

from blitz.ui.pages.base import BasePage


class BlitzRouter:
    def __init__(self, base_url: str = "/") -> None:
        self.base_url = base_url

    def add_page(self, url: str, component: Type[BasePage]) -> None:
        ui.page(f"{self.base_url}{url}")(component.entrypoint)
