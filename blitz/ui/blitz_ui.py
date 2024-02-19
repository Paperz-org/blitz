from functools import lru_cache
from pathlib import Path
from typing import Any
from blitz.app import BlitzApp
from blitz.core import BlitzCore
from blitz.settings import Settings, get_settings
from blitz.tools.erd import generate_mermaid_erd


# @lru_cache
# def get_erd(app: BlitzApp) -> str:
#     return generate_mermaid_erd(app._base_resource_model.metadata)


class BlitzUI:
    def __init__(self, settings: Settings = get_settings()) -> None:
        self.blitz_app: BlitzCore = BlitzCore()
        self.apps = self.blitz_app.apps
        self.preprompt = self._get_preprompt()

        self.settings = settings
        self.localhost_url = f"http://localhost:{settings.BLITZ_PORT}"
        self.erd: str | None = None
        self._current_project: str | None = None
        self._current_app: BlitzApp | None = None

    @property
    def current_project(self) -> str | None:
        return self._current_project

    @current_project.setter
    def current_project(self, project: str) -> None:
        print(project)
        self._current_project = project

    @property
    def current_app(self) -> BlitzApp | None:
        return self._current_app

    @current_app.setter
    def current_app(self, app: BlitzApp) -> None:
        if not self.current_app:
            self._current_app = app
            self._current_project = app.name
            self.erd = generate_mermaid_erd(app._base_resource_model.metadata)

    # @current_project.setter
    # def current_project(self, project):
    #     if project and project != self.current_project:
    #         self._current_project = project
    #         self._current_app = self.get_current_app()

    def get_ressources(self) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        columns = [
            {
                "name": "name",
                "label": "Name",
                "field": "name",
                "required": True,
                "align": "left",
                "sortable": True,
            },
            {
                "name": "allowed_methods",
                "label": "Allowed Methods",
                "field": "allowed_methods",
                "sortable": True,
            },
        ]
        rows = []
        if self.current_app is None:
            # TODO handle error
            raise Exception
        for ressource in self.current_app.resources:
            rows.append(
                {
                    "name": ressource.config.name,
                    "allowed_methods": ressource.config.settings.allowed_methods,
                }
            )

        return columns, rows

    def get_current_app(self) -> BlitzApp | None:
        if self.current_project:
            return self.blitz_app.get_app(self.current_project)
        return None

    def add(self, blitz_app: BlitzCore) -> None:
        self.blitz_app = blitz_app

    def _get_preprompt(self) -> str:
        with open(Path(__file__).parent / "./preprompt.txt", "r") as f:
            return f.read()

    def reset_preprompt(self) -> None:
        self.preprompt = self._get_preprompt()
        print(self.preprompt)


@lru_cache
def get_blitz_ui() -> BlitzUI:
    return BlitzUI()
