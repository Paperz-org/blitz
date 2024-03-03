from functools import lru_cache
from fastapi import FastAPI
from starlette_admin import CustomView
from blitz.db.db import get_sqlite_engine
from starlette_admin.contrib.sqla import Admin, ModelView
from typing import TYPE_CHECKING, Any, List
from starlette_admin.views import Link
from starlette.responses import Response
from starlette.requests import Request
from blitz.settings import Settings, get_settings
from starlette.templating import Jinja2Templates

if TYPE_CHECKING:
    from blitz.app import BlitzApp


class HomeView(CustomView):
    def __init__(self, blitz_app: "BlitzApp", *args: Any, **kwargs: Any):
        self.blitz_app = blitz_app
        super().__init__(*args, **kwargs)

    async def render(
        self,
        request: Request,
        templates: Jinja2Templates,
    ) -> Response:
        return templates.TemplateResponse("index.html", {"request": request, "blitz_app": self.blitz_app})


class BlitzAdmin:
    def __init__(self, blitz_app: "BlitzApp", settings: Settings = get_settings()) -> None:
        self.blitz_app = blitz_app
        self.admin = Admin(
            title=f"Blitz Admin - {blitz_app.name}",
            # FIXME find a better way to get the engine
            engine=get_sqlite_engine(blitz_app, in_memory=blitz_app._in_memory, file_name="app.db"),
            base_url="/admin/",
            templates_dir="blitz/api/templates",
            index_view=HomeView(blitz_app, "Home"),
            statics_dir="blitz/ui/assets/",
            logo_url="/admin/statics/blitz_logo_and_text_2.png",
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
        self.admin.add_view(Link(label="GitHub", icon="fa-brands fa-github", url="https://github.com/Paperz-org/blitz"))
        self.admin.add_view(Link(label="Documentation", icon="fa fa-book", url="https://paperz-org.github.io/blitz/"))

    def mount_to(self, app: FastAPI) -> None:
        self.admin.mount_to(app)
