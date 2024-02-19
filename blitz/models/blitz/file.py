from typing import Any, ClassVar, NoReturn
from pydantic import BaseModel, Field, ValidationError, field_serializer
from blitz.models.blitz.config import BlitzAppConfig
from blitz.models.blitz.resource import BlitzResourceConfig
from pathlib import Path
from enum import StrEnum
import json
import yaml


def _get_data_from_json(file: Path) -> dict[str, dict[str, Any]]:
    with open(file, "r") as f:
        return dict(json.load(f))


def _get_data_from_yaml(file: Path) -> dict[str, dict[str, Any]]:
    with open(file, "r") as f:
        return dict(yaml.safe_load(f))


def _no_parser_for_suffix(file: Path) -> NoReturn:
    raise ValueError(f"No parser for {file}")


class BlitzFile(BaseModel):
    """
    The Blitz file is the configuration file for a Blitz app. It contains the BlitzAppConfig and a list of BlitzResourceConfig.
    """

    class FileType(StrEnum):
        JSON = "json"
        YAML = "yaml"

    CONFIG_FIELD_NAME: ClassVar[str] = "config"
    RESOURCES_FIELD_NAME: ClassVar[str] = "resources"

    config: BlitzAppConfig
    resources_configs: list[BlitzResourceConfig] = Field(
        default=[], serialization_alias=RESOURCES_FIELD_NAME
    )
    raw_file: dict[str, Any] = Field(exclude=True)
    path: Path | None = Field(default=None, exclude=True)
    file_type: FileType | None = Field(default=None, exclude=True)

    # def write(self) -> None:
    #     with open(self.path, "w") as blitz_file:
    #         blitz_file.write(self.model_dump_json)

    @field_serializer("resources_configs")
    def _serialize_resources_configs(
        self, resources_configs: list[BlitzResourceConfig], _info: Any
    ) -> dict[str, Any]:
        serialized_resources_configs = {}
        for resource_config in resources_configs:
            serialized_resources_configs[resource_config.name] = (
                resource_config.model_dump()
            )

        return serialized_resources_configs

    @classmethod
    def from_file(cls, file_path: Path) -> "BlitzFile":
        blitz_file = {
            cls.FileType.JSON.value: _get_data_from_json,
            cls.FileType.YAML.value: _get_data_from_yaml,
        }.get(file_path.suffix[1:], _no_parser_for_suffix)(file_path)

        return cls.from_dict(
            blitz_file,
            path=file_path.absolute(),
            file_type=cls.FileType(file_path.suffix.removeprefix(".")),
        )

    @classmethod
    def from_dict(
        cls,
        blitz_file: dict[str, dict[str, Any]],
        path: Path | None = None,
        file_type: FileType | None = None,
    ) -> "BlitzFile":
        resources_configs: list[BlitzResourceConfig] = []
        resource_name: str
        resource_config: dict[str, Any]

        for resource_name, resource_config in blitz_file.get(
            cls.RESOURCES_FIELD_NAME, {}
        ).items():
            settings_fields = {}
            fields = {}
            for field_name, field_value in resource_config.items():
                if field_name.startswith(BlitzResourceConfig.Settings.FIELD_PREFIX):
                    settings_fields[
                        field_name[len(BlitzResourceConfig.Settings.FIELD_PREFIX) :]
                    ] = field_value
                else:
                    fields[field_name] = field_value
            resources_configs.append(
                BlitzResourceConfig(
                    name=resource_name, fields=fields, settings=settings_fields
                )
            )

        return cls(
            config=blitz_file.get(cls.CONFIG_FIELD_NAME),
            resources_configs=resources_configs,
            raw_file=blitz_file,
            path=path,
            file_type=file_type,
        )
