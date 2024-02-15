from fastapi import FastAPI
from blitz.db.db import get_sqlite_engine
from starlette_admin.contrib.sqla import Admin, ModelView
from typing import TYPE_CHECKING
from starlette_admin.views import Link

from blitz.settings import Settings, get_settings

if TYPE_CHECKING:
    from blitz.app import BlitzApp


class BlitzAdmin:
    def __init__(
        self, blitz_app: "BlitzApp", settings: Settings = get_settings()
    ) -> None:
        self.blitz_app = blitz_app
        self.admin = Admin(
            title=f"{blitz_app.name} Admin",
            # FIXME find a better way to get the engine
            engine=get_sqlite_engine(
                blitz_app, in_memory=blitz_app._in_memory, file_name="app.db"
            ),
            base_url=f"/admin/",
        )
        for resource in blitz_app.resources:
            self.admin.add_view(ModelView(resource.model))

        self.admin.add_view(
            Link(
                label="Go Back to Dashboard",
                icon="fa fa-link",
                url=f"http://localhost:{settings.BLITZ_PORT}/dashboard/projects/{self.blitz_app.name}",
            )
        )

    def mount_to(self, app: FastAPI) -> None:
        self.admin.mount_to(app)
