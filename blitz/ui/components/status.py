from nicegui import ui

from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from httpx import AsyncClient


class StatusComponent:
    def __init__(self, blitz_ui: BlitzUI = get_blitz_ui()) -> None:
        self.blitz_ui = blitz_ui
        self.app = self.blitz_ui.current_app
        self.api_up = False
        self.admin_up = False
        ui.timer(10.0, self.set_status)

    async def _is_api_up(self):
        async with AsyncClient() as client:
            response = await client.get(f"{self.blitz_ui.localhost_url}/api")
            return response.status_code == 200

    async def _is_admin_up(self):
        async with AsyncClient() as client:
            response = await client.get(f"{self.blitz_ui.localhost_url}/admin/")
            return response.status_code == 200

    async def set_status(self):
        self.api_up = await self._is_api_up()
        self.admin_up = await self._is_admin_up()
        self.render.refresh()

    @ui.refreshable
    def render(self):
        with ui.grid(rows=2, columns=2).classes("gap-4"):
            ui.label(f"API:").classes("text-lg font-bold")
            if self.api_up:
                ui.icon(name="check_circle").classes("text-green-500")
            else:
                ui.icon(name="error").classes("text-red-500")
            ui.label(f"Admin:").classes("text-lg font-bold")
            if self.admin_up:
                ui.icon(name="check_circle").classes("text-green-500")
            else:
                ui.icon(name="error").classes("text-red-500")
