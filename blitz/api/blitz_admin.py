from pathlib import Path
from typing import TYPE_CHECKING, Any

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.templating import Jinja2Templates
from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.views import Link

from blitz.db.session import get_engine
from blitz.settings import Settings, get_settings

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
    TEMPLATES_DIR_PATH = str((Path(__file__).parent / "templates").absolute())
    STATIC_DIR_PATH = str((Path(__file__).parent.parent / "ui/assets").absolute())

    def __init__(self, blitz_app: "BlitzApp", settings: Settings = get_settings()) -> None:
        self.blitz_app = blitz_app
        self.admin = Admin(
            title=f"Blitz Admin - {blitz_app.name}",
            # FIXME find a better way to get the engine
            engine=get_engine(blitz_app, settings.BLITZ_DB_TYPE),
            base_url="/admin/",
            templates_dir=self.TEMPLATES_DIR_PATH,
            index_view=HomeView(blitz_app, "Home"),
            statics_dir=self.STATIC_DIR_PATH,
            logo_url="/admin/statics/blitz_logo_and_text_2.png",
        )
        for resource in blitz_app.resources:
            self.admin.add_view(ModelView(resource.model))

        self.admin.add_view(
            Link(
                label="Go Back to Dashboard",
                icon="fa fa-link",
                url=f"/dashboard/projects/{self.blitz_app.name}",
            )
        )
        self.admin.add_view(Link(label="GitHub", icon="fa-brands fa-github", url="https://github.com/Paperz-org/blitz"))
        self.admin.add_view(Link(label="Documentation", icon="fa fa-book", url="https://paperz-org.github.io/blitz/"))

    def mount_to(self, app: FastAPI) -> None:
        self.admin.mount_to(app)
