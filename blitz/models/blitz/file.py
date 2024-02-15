from typing import Any, ClassVar
from pydantic import BaseModel, Field
from blitz.models.blitz.config import BlitzAppConfig
from blitz.models.blitz.resource import BlitzResourceConfig
from pathlib import Path
from enum import StrEnum

class FileType(StrEnum):
    JSON = "json"
    YAML = "yaml"

class BlitzFile(BaseModel):
    """
    The Blitz file is the configuration file for a Blitz app. It contains the BlitzAppConfig and a list of BlitzResourceConfig.
    """

    path: Path | None = Field(None, exclude=True)
    file_type: FileType | None = Field(None, exclude=True)
    config: BlitzAppConfig
    resources_configs: list[BlitzResourceConfig] = Field(
        [], serialization_alias="resources"
    )
    raw_file: dict = Field(exclude=True)

    # def write(self) -> None:
    #     with open(self.path, "w") as blitz_file:
    #         blitz_file.write(self.model_dump_json)
