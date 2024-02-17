from typing import Any, ClassVar
from pydantic import BaseModel, field_validator, model_serializer
from blitz.models.blitz.field import BlitzField
from blitz.models.base import BaseResourceModel


class BlitzResourceConfig(BaseModel):
    """
    The BlitzResourceConfig is the configuration of a BlitzResource. It contains the name of the resource, the allowed
    methods and the fields. The fields can be a string or a BlitzField object.
    If the fields is a string, we are reading it like a shortcut version of a BlitzField object.
    """

    class Settings(BaseModel):
        FIELD_PREFIX: ClassVar[str] = "_"
        allowed_methods: str = "CRUD"
        description: str | None = None

    name: str
    fields: dict[str, BlitzField]
    settings: Settings = Settings()

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
                settings_fields_config = {}
                field_config = {}
                for field_config_name, field_config_value in raw_field_value.items():
                    if field_config_name.startswith(BlitzField.Settings.FIELD_PREFIX):
                        settings_fields_config[
                            field_config_name[len(BlitzField.Settings.FIELD_PREFIX) :]
                        ] = field_config_value
                    else:
                        field_config[field_config_name] = field_config_value
                fields[field_name] = BlitzField(
                    _raw_field_name=raw_field_name,
                    _raw_field_value=raw_field_value,
                    settings=settings_fields_config,
                    **field_config,
                )
            else:
                raise ValueError(f"Type `{type(raw_field_value)}` not allowed for field `{raw_field_name}`")
        return fields

    @model_serializer
    def _serialize_model(self) -> dict[str, Any]:
        serialized_model = {}
        for field_name, field in self.fields.items():
            serialized_model[field_name] = field.model_dump(exclude_unset=True)
        for setting_name, setting_value in self.settings.model_dump(exclude_unset=True).items():
            serialized_model[f"{self.Settings.FIELD_PREFIX}{setting_name}"] = setting_value
        return serialized_model

    @property
    def can_create(self) -> bool:
        return "C" in self.settings.allowed_methods

    @property
    def can_read(self) -> bool:
        return "R" in self.settings.allowed_methods

    @property
    def can_update(self) -> bool:
        return "U" in self.settings.allowed_methods

    @property
    def can_delete(self) -> bool:
        return "D" in self.settings.allowed_methods


class BlitzResource(BaseModel):
    """
    The BlitzResource is the representation of a resource in Blitz. It contains the configuration used to generate the resource
    and the SQLmodel class.
    """

    config: BlitzResourceConfig
    model: type[BaseResourceModel]


BlitzResourceConfig(
    name="Food",
    fields={
        "name!": "str!",
        "expiration_date": "datetime!",
    },
    settings={},
)

BlitzResourceConfig(
    name="Ingredient",
    fields={
        "food_id": "Food.id",
        "food": "Food",
        "recipe_id": "Recipe.id!",
        "recipe": "Recipe",
    },
    settings={},
)

BlitzResourceConfig(
    name="Recipe",
    fields={
        "name!": "str!",
        "ingredients": "Ingredient[]",
        "cook_id": "Cook.id!",
        "cook": "Cook",
    },
    settings={},
)

BlitzResourceConfig(
    name="Cook",
    fields={
        "name!": "str!",
        "age": "int!",
        "recipes": "Recipe[]",
        "rat": "Rat",
    },
    settings={},
)

BlitzResourceConfig(
    name="Rat",
    fields={
        "name!": "str!",
        "age": "int!",
        "cook_id!": "Cook.id!",
        "cook": "Cook",
    },
    settings={},
)
