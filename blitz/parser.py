from pathlib import Path

from blitz.models.blitz import BlitzFile


def find_blitz_app_path(blitz_app_name: str) -> Path:
    blitz_app_path = (Path(".") / Path(blitz_app_name)).absolute()
    if not blitz_app_path.is_dir():
        raise FileNotFoundError(f"Could not find a Blitz app in {blitz_app_path}.")
    return blitz_app_path


def find_blitz_file_path(blitz_app_path: Path) -> Path:
    blitz_file_path: Path | None = None
    for type in BlitzFile.FileType:
        blitz_file = blitz_app_path / f"blitz.{type.value}"
        if blitz_file.exists():
            if blitz_file_path is not None:
                raise ValueError(f"Found multiple Blitz files in {blitz_app_path}.")
            blitz_file_path = blitz_file

    if blitz_file_path is None:
        raise FileNotFoundError(f"Could not find a Blitz file in {blitz_app_path}.")
    return blitz_file_path
