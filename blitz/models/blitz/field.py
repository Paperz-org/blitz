import enum
from blitz.models.utils import ContainsEnum
from typing import Any, ClassVar

from pydantic import BaseModel, Field, computed_field, field_validator, model_serializer
import uuid
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class _BlitzNullValue:
    """
    This class is used to represent a null value in BlitzField.
    """

    ...


class AllowedBlitzFieldTypes(enum.StrEnum, metaclass=ContainsEnum):
    str = "str"
    int = "int"
    float = "float"
    uuid = "uuid"
    datetime = "datetime"
    foreign_key = "foreign_key"
    relationship = "relationship"

    @classmethod
    def from_class(cls, v: Any) -> "AllowedBlitzFieldTypes":
        return cls(v.__name__.lower())


class BlitzType(BaseModel):
    TYPE_MAPPING: ClassVar[dict[AllowedBlitzFieldTypes, Any]] = {
        AllowedBlitzFieldTypes.str: str,
        AllowedBlitzFieldTypes.int: int,
        AllowedBlitzFieldTypes.float: float,
        AllowedBlitzFieldTypes.uuid: uuid.UUID,
        AllowedBlitzFieldTypes.datetime: datetime,
    }
    TYPE_FACTORY_MAPPING: ClassVar[dict[AllowedBlitzFieldTypes, Any]] = {
        AllowedBlitzFieldTypes.str: lambda: "string",
        AllowedBlitzFieldTypes.int: int,
        AllowedBlitzFieldTypes.float: float,
        AllowedBlitzFieldTypes.uuid: uuid.uuid4,
        AllowedBlitzFieldTypes.datetime: datetime.now,
    }
    type: AllowedBlitzFieldTypes

    def __init_subclass__(cls, **kwargs: Any) -> None:
        for allowed_type in AllowedBlitzFieldTypes:
            if allowed_type not in cls.TYPE_MAPPING:
                logger.warning(f"Type {allowed_type} is not mapped with a factory in {cls.__name__}.TYPE_MAPPING.")

    @computed_field  # type: ignore
    @property
    def value(self) -> Any:
        return self.TYPE_MAPPING.get(self.type, None)

    @computed_field  # type: ignore
    @property
    def factory(self) -> Any:
        return self.TYPE_FACTORY_MAPPING.get(self.type, None)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type='{self.type}')"

    def __eq__(self, __value: object) -> bool:
        return self.type.value == __value

    @model_serializer
    def _serialize_model(self) -> str:
        return self.type.value


class BlitzField(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    # Modifiers are used to define the properties of a field in the shortcut version of the blitz field
    _unique_modifier: ClassVar[str] = "!"
    _nullable_modifier: ClassVar[str] = "?"
    _required_modifier: ClassVar[str] = "!"
    _relationship_list_modifier: ClassVar[str] = "[]"

    _field_name_shortcut_modifiers: ClassVar[str] = "".join(_unique_modifier)
    _field_value_shortcut_modifiers: ClassVar[str] = "".join(
        [
            _nullable_modifier,
            _required_modifier,
            _relationship_list_modifier,
        ]
    )

    # We store the raw values for writing them back in the blitz file
    _raw_field_name: str | None = None
    _raw_field_value: str | dict[str, Any] | None = None

    type: BlitzType
    default: Any = Field(_BlitzNullValue(), exclude=True)
    foreign_key: str | _BlitzNullValue = Field(_BlitzNullValue(), exclude=True)
    relationship: str | _BlitzNullValue = Field(_BlitzNullValue(), exclude=True)
    relationship_list: bool | _BlitzNullValue = Field(_BlitzNullValue(), exclude=True)
    back_populates: str | _BlitzNullValue = Field(_BlitzNullValue(), exclude=True)
    nullable: bool | _BlitzNullValue = Field(_BlitzNullValue(), exclude=True)
    unique: bool | _BlitzNullValue = Field(_BlitzNullValue(), exclude=True)

    @field_validator("type", mode="before")
    def _string_to_customtype(cls, v: str | BlitzType) -> BlitzType:
        if isinstance(v, str):
            return BlitzType(type=AllowedBlitzFieldTypes(v))
        return v

    # Need a fix in pydantic maybe use a custom method to serialize the model and not the @model_serializer
    # @model_serializer
    # def _serialize_model(self) -> dict[str, Any] | str:
    #     if isinstance(self._raw_field_value, dict):
    #         return self.model_dump()
    #     elif isinstance(self._raw_field_value, str):
    #         return self.model_shortcut_dump()
    #     else:
    #         raise ValueError(f"Type `{type(self._raw_field_value)}` not allowed")

    @classmethod
    def from_shortcut_version(cls, raw_field_name: str, raw_field_value: str) -> "BlitzField":
        field_name = raw_field_name.strip(cls._field_name_shortcut_modifiers)
        field_name_modifiers = raw_field_name[len(field_name) :]

        field_value = raw_field_value.strip(cls._field_value_shortcut_modifiers)
        field_value_modifiers = raw_field_value[len(field_value) :]

        if cls._required_modifier in field_value_modifiers and cls._nullable_modifier in field_value_modifiers:
            raise ValueError(f"Field `{field_name}` cannot be both required and nullable.")

        if field_value in AllowedBlitzFieldTypes:
            field_type = AllowedBlitzFieldTypes(field_value)
        elif "." in field_value:
            field_type = AllowedBlitzFieldTypes.foreign_key
        else:
            field_type = AllowedBlitzFieldTypes.relationship

        return cls(
            _raw_field_name=raw_field_name,
            _raw_field_value=raw_field_value,
            type=field_type,  # type: ignore
            nullable=cls._nullable_modifier in field_value_modifiers,
            unique=cls._unique_modifier in field_name_modifiers,
            default=None if cls._nullable_modifier in field_value_modifiers else _BlitzNullValue(),
            foreign_key=field_value if field_type == AllowedBlitzFieldTypes.foreign_key else _BlitzNullValue(),
            relationship=field_value if field_type == AllowedBlitzFieldTypes.relationship else _BlitzNullValue(),
            relationship_list=(
                cls._relationship_list_modifier in field_value_modifiers
                if field_type == AllowedBlitzFieldTypes.relationship
                else _BlitzNullValue()
            ),
        )

    def model_shortcut_dump(self) -> str:
        modifiers = []

        if self.relationship_list is True:
            modifiers.append(self._relationship_list_modifier)

        if self.nullable is True:
            modifiers.append(self._nullable_modifier)
        elif self.nullable is False:
            modifiers.append(self._required_modifier)

        return f"{self.type}{''.join(modifiers)}"
