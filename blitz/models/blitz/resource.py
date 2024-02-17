from typing import Any
from pydantic import BaseModel, field_validator
from blitz.models.blitz.field import BlitzField
from blitz.models.base import BaseResourceModel


class BlitzResourceConfig(BaseModel):
    """
    The BlitzResourceConfig is the configuration of a BlitzResource. It contains the name of the resource, the allowed
    methods and the fields. The fields can be a string or a BlitzField object.
    If the fields is a string, we are reading it like a shortcut version of a BlitzField object.
    """

    name: str
    allowed_methods: str = "CRUD"
    fields: dict[str, BlitzField]

    @field_validator("fields", mode="before")
    def _string_to_fields(cls, v: dict[str, Any | dict[str, Any]]) -> dict[str, BlitzField]:
        fields: dict[str, BlitzField] = {}
        for raw_field_name, raw_field_value in v.items():
            field_name = raw_field_name.strip(BlitzField._field_name_shortcut_modifiers)
            # If the field values is a string, it can be an blitz type or a relationship related field
            if isinstance(raw_field_value, str):
                fields[field_name] = BlitzField.from_shortcut_version(raw_field_name, raw_field_value)

            # Else if the field value is a dict, it must be a BlitzField object
            elif isinstance(raw_field_value, dict):
                fields[field_name] = BlitzField(
                    _raw_field_name=raw_field_name,
                    _raw_field_value=raw_field_value,
                    **raw_field_value,
                )
            else:
                raise ValueError(f"Type `{type(raw_field_value)}` not allowed for field `{raw_field_name}`")
        return fields

    @property
    def can_create(self) -> bool:
        return "C" in self.allowed_methods

    @property
    def can_read(self) -> bool:
        return "R" in self.allowed_methods

    @property
    def can_update(self) -> bool:
        return "U" in self.allowed_methods

    @property
    def can_delete(self) -> bool:
        return "D" in self.allowed_methods


class BlitzResource(BaseModel):
    """
    The BlitzResource is the representation of a resource in Blitz. It contains the configuration used to generate the resource
    and the SQLmodel class.
    """

    config: BlitzResourceConfig
    model: type[BaseResourceModel]
