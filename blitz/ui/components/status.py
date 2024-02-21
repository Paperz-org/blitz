from typing import Any
from nicegui import ui

from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from httpx import AsyncClient

from blitz.ui.components.base import BaseComponent


class StatusComponent(BaseComponent[ui.grid], reactive=True):
    api_up: bool = False
    admin_up: bool = False

    def __init__(self, *args: Any, props: str = "", classes: str = "", **kwargs: Any) -> None:
        ui.timer(10.0, self._set_status)
        super().__init__(*args, props=props, classes=classes, **kwargs)

    async def _is_api_up(self) -> bool:
        async with AsyncClient() as client:
            response = await client.get(f"{self.blitz_ui.localhost_url}/api")
            return response.status_code == 200

    async def _is_admin_up(self) -> bool:
        async with AsyncClient() as client:
            response = await client.get(f"{self.blitz_ui.localhost_url}/admin/")
            return response.status_code == 200

    async def _set_status(self) -> None:
        self.api_up = await self._is_api_up()
        self.admin_up = await self._is_admin_up()

    def render(self) -> None:  # type: ignore
        with ui.grid(rows=2, columns=2).classes("gap-4") as self.ng:
            ui.label("API:").classes("text-lg font-bold")
            if self.api_up:
                ui.icon(name="check_circle").classes("text-green-500")
            else:
                ui.icon(name="error").classes("text-red-500")
            ui.label("Admin:").classes("text-lg font-bold")
            if self.admin_up:
                ui.icon(name="check_circle").classes("text-green-500")
            else:
                ui.icon(name="error").classes("text-red-500")

