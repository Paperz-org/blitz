from typing import Any
from nicegui import ui

from httpx import AsyncClient

from blitz.ui.components.base import BaseComponent
from blitz.ui.components.grids.base import BaseGrid as Grid
from blitz.ui.components.icon.base import BaseIcon as Icon
from blitz.ui.components.labels.base import TextLgBoldLabel
from blitz.ui.components.timer.base import BaseTimer as Timer


class StatusComponent(BaseComponent[Grid], reactive=True):
    _GreenIcon = Icon("check_circle", classes="text-green-500", render=False)
    _RedIcon = Icon("error", classes="text-red-500", render=False)

    api_up: bool = False
    admin_up: bool = False

    def __init__(
        self,
        *args: Any,
        props: str = "",
        classes: str = "",
        **kwargs: Any,
    ) -> None:
        Timer(10.0, self._set_status)
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
        self.refresh()

    def render(self) -> None:
        with Grid(rows=2, columns=2, classes="gap-4") as self.ng:  # type: ignore
            TextLgBoldLabel("API:")
            self._GreenIcon() if self.api_up else self._RedIcon()
            TextLgBoldLabel("Admin:")
            self._GreenIcon() if self.admin_up else self._RedIcon()
