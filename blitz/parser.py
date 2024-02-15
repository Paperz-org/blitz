import json
from pathlib import Path

import yaml
from typing import Any, NoReturn

from blitz.models.blitz import BlitzFile


def _get_data_from_json(file: Path) -> dict[str, Any]:
    with open(file, "r") as f:
        return dict(json.load(f))


def _get_data_from_yaml(file: Path) -> dict[str, Any]:
    with open(file, "r") as f:
        return dict(yaml.safe_load(f))


def _no_parser_for_suffix(file: Path) -> NoReturn:
    raise ValueError(f"No parser for {file}")


def _find_blitz_app_path(blitz_app_name: str) -> Path:
    blitz_app_path = (Path(".") / Path(blitz_app_name)).absolute()
    if not blitz_app_path.is_dir():
        raise FileNotFoundError(f"Could not find a Blitz app in {blitz_app_path}.")
    return blitz_app_path


def _find_blitz_file_path(blitz_app_path: Path) -> Path:
    yaml_blitz_file = blitz_app_path / "blitz.yaml"
    json_blitz_file = blitz_app_path / "blitz.json"

    if yaml_blitz_file.exists() and json_blitz_file.exists():
        raise ValueError(
            f"Found both a YAML and a JSON Blitz file in {blitz_app_path}."
        )
    if yaml_blitz_file.exists():
        return yaml_blitz_file
    elif json_blitz_file.exists():
        return json_blitz_file
    else:
        raise FileNotFoundError(f"Could not find a Blitz file in {blitz_app_path}.")


def parse_file(file_path: Path) -> BlitzFile:
    blitz_file_fields = {
        ".json": _get_data_from_json,
        ".yaml": _get_data_from_yaml,
    }.get(file_path.suffix, _no_parser_for_suffix)(file_path)
    return BlitzFile(
        path=file_path.absolute(),
        file_type=file_path.suffix.removeprefix("."),
        config=blitz_file_fields["config"],
        resources_configs=blitz_file_fields["resources"],
        raw_file=blitz_file_fields,
    )


def create_blitz_file_from_dict(blitz_file_content: dict) -> BlitzFile:
    return BlitzFile(
        config=blitz_file_content.get("config"),
        resources_configs=blitz_file_content.get("resources"),
        raw_file=blitz_file_content,
    )
