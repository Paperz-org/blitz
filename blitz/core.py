from pathlib import Path

from blitz.app import BlitzApp
from blitz.parser import _find_blitz_app_path, _find_blitz_file_path, parse_file
from blitz.settings import DBTypes, get_settings


class BlitzCore:
    BLITZ_DOT_FILE = ".blitz"

    def __init__(self) -> None:
        self.apps: list[BlitzApp] = []
        self._discover_apps()

    def get_app(self, name: str) -> BlitzApp:
        for app in self.apps:
            if app.name == name:
                return app
        raise Exception(f"Blitz app {name} not found.")

    def _discover_apps(self) -> None:
        """
        Discovers Blitz apps in the current directory and its subdirectories.
        """

        for dotfile in Path(".").glob(f"**/*{self.BLITZ_DOT_FILE}"):
            blitz_app_name = dotfile.parent.name
            blitz_app_path = _find_blitz_app_path(blitz_app_name)
            blitz_file_path = _find_blitz_file_path(blitz_app_path)
            blitz_file = parse_file(blitz_file_path)

            self.apps.append(
                BlitzApp(
                    blitz_app_name,
                    blitz_app_path,
                    blitz_file,
                    in_memory=get_settings().BLITZ_DB_TYPE == DBTypes.MEMORY,
                )
            )
