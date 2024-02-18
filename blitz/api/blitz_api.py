from functools import partial
import os
from typing import Any

import warnings

from fastapi.responses import RedirectResponse
from blitz.api.blitz_admin import BlitzAdmin
from blitz.core import BlitzCore
from blitz.db.db import get_db
from blitz.db.errors import NoChangesDetectedError
from blitz.app import BlitzApp
from fastapi import FastAPI, APIRouter
from fastapi_crudrouter.core import CRUDGenerator  # type: ignore
from fastapi_crudrouter import SQLAlchemyCRUDRouter  # type: ignore
from semver import Version
from blitz.models.blitz.resource import BlitzResource
from blitz.patch import patch_fastapi_crudrouter
from blitz.settings import DBTypes, get_settings
from blitz.db.migrations import generate_migration, run_migrations
from blitz.api.logs import configure as configure_logs
from rich import print

from sqlalchemy.exc import SAWarning

# Patch the crudrouter to work with pydantic v2
patch_fastapi_crudrouter()


class BlitzAPI(FastAPI):
    def __init__(
        self,
        blitz_app: BlitzApp,
        enable_config_route: bool = True,
        *args: Any,
        docs_url: str = "/api/docs",
        redoc_url: str = "/api/redoc",
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, docs_url=docs_url, redoc_url=redoc_url, **kwargs)
        self.blitz_app = blitz_app
        self.blitz_app.load()
        self.logger = self.blitz_app.logger

        if enable_config_route:
            self.include_router(self._create_blitz_config_router())

        for resource in self.blitz_app.resources:
            router = self._create_crud_router(resource=resource)
            self.include_router(router, prefix="/api")

        self._add_healthcheck()
        self._add_redirect()

        configure_logs(self)

    def _add_healthcheck(self) -> None:
        self.router.add_api_route(
            "/api",
            lambda: {"status": "ok"},
            methods=["GET"],
            tags=["health"],
            include_in_schema=False,
        )

    def _add_redirect(self) -> None:
        self.router.add_api_route(
            "/",
            lambda: RedirectResponse(f"/dashboard/projects/{self.blitz_app.name}"),
            methods=["GET"],
            include_in_schema=False,
        )

    def _create_blitz_config_router(self) -> APIRouter:
        path = "/blitz-config"
        router = APIRouter()
        router.add_api_route(
            path=path,
            endpoint=lambda: self.blitz_app.file.model_dump(by_alias=True),
            methods=["GET"],
            summary="Get Blitz Config",
            description="Returns the Blitz Config for all resources",
        )
        return router

    def _create_crud_router(self, resource: BlitzResource) -> CRUDGenerator:
        read_model = resource.model.read_model()
        create_model = resource.model.create_model()
        update_model = resource.model.update_model()

        # Rebuild the model to include forward ref types that was not available at the time of the model creation
        # We need to use the model AFTER the rebuild because if not, all the relationship and cie will not be set
        # correctly.
        types_namespace = {
            resource.model.__name__: resource.model
            for resource in self.blitz_app.resources
        }
        read_model.model_rebuild(_types_namespace=types_namespace)
        create_model.model_rebuild(_types_namespace=types_namespace)
        update_model.model_rebuild(_types_namespace=types_namespace)
        resource.model.model_rebuild(_types_namespace=types_namespace)

        return SQLAlchemyCRUDRouter(
            schema=read_model,
            create_schema=create_model,
            update_schema=update_model,
            db_model=resource.model,
            db=partial(
                get_db,
                self.blitz_app,
                get_settings().BLITZ_DB_TYPE == DBTypes.MEMORY,
                "app.db",
            ),
            delete_all_route=False,
            get_all_route=resource.config.can_read,
            get_one_route=resource.config.can_read,
            update_route=resource.config.can_update,
            create_route=resource.config.can_create,
            delete_one_route=resource.config.can_delete,
        )


def create_blitz_api(
    blitz_app: BlitzApp | None = None,
    enable_config_route: bool = True,
    admin: bool = True,
    *args: Any,
    docs_url: str = "/api/docs",
    redoc_url: str = "/api/redoc",
    **kwargs: Any,
) -> BlitzAPI:
    from blitz.ui.main import init_ui

    blitz_app_version = None
    if blitz_app is None:
        blitz = BlitzCore()
        blitz_app_name = os.getenv("BLITZ_APP")
        blitz_app_version = os.getenv("BLITZ_VERSION")
        if blitz_app_name is None:
            raise Exception("No blitz app name provided.")
        enable_config_route = os.getenv("BLITZ_CONFIG_ROUTE", "").lower() == "true"
        admin = os.getenv("BLITZ_ADMIN", "").lower() == "true"
        blitz_app = blitz.get_app(blitz_app_name)
        if blitz_app_version is not None:
            blitz_app = blitz_app.get_version(Version.parse(blitz_app_version))

    # TODO Maybe to remove
    blitz_app.load()
    blitz_api = BlitzAPI(
        blitz_app,
        enable_config_route,
        *args,
        docs_url=docs_url,
        redoc_url=redoc_url,
        **kwargs,
    )

    if not blitz_app_version:
        run_migrations(
            blitz_app=blitz_app,
            in_memory=blitz_app._in_memory,
        )

        try:
            generate_migration(
                message="Blitz autogenerated migration",
                blitz_app=blitz_app,
                in_memory=blitz_app._in_memory,
            )
        except NoChangesDetectedError:
            pass
        else:
            run_migrations(
                blitz_app=blitz_app,
                in_memory=blitz_app._in_memory,
            )
    else:
        run_migrations(
            blitz_app=blitz_app,
            in_memory=blitz_app._in_memory,
            is_release=True,
        )

    if admin:
        # FIXME We need to fix the the relationship here.
        # Proposed solution: "To silence this warning, add the parameter 'overlaps="todos"' to the 'Todo.todo_list' relationship."
        # https://docs.sqlalchemy.org/en/20/errors.html#error-qzyx
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=SAWarning)
            BlitzAdmin(blitz_app).mount_to(blitz_api)

    print(
        "\n[bold yellow]This is still an alpha. Please do not use in production.[/bold yellow]"
    )
    print(
        "[bold yellow]Please report any issues on https://github.com/Paperz-org/blitz[/bold yellow]"
    )
    print(
        "\n".join(
            (
                "\n[bold medium_purple1]Blitz app deployed.",
                f"  - Blitz UI            : http://localhost:{get_settings().BLITZ_PORT}",
                f"  - Blitz admin         : http://localhost:{get_settings().BLITZ_PORT}/admin",
                f"  - Swagger UI          : http://localhost:{get_settings().BLITZ_PORT}/api/docs[/bold medium_purple1]\n",
            )
        )
    )

    init_ui(blitz_api=blitz_api)
    return blitz_api
