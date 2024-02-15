from typing import Optional, TypeVar
import typing
import uuid
from sqlalchemy.orm import declared_attr
from pydantic import BaseModel, create_model
from uuid import UUID
from sqlmodel import Relationship, SQLModel, Field
from pydantic.fields import FieldInfo
from types import UnionType
from blitz.models.blitz.field import _BlitzNullValue, AllowedBlitzFieldTypes
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from blitz.models.blitz.resource import BlitzResourceConfig

T = TypeVar("T", bound="BaseModel")


class BaseResourceModel(SQLModel):
    """
    Base class for SQL models.

    Attributes:
        id (UUID): The primary key of the model.
    """

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        """
        Get the table name for the model.

        Returns:
            str: The table name.
        """
        return cls.__name__

    id: UUID = Field(
        default_factory=uuid.uuid4,
        description="Unique identifier for this resource.",
        primary_key=True,
        index=True,
        nullable=False,
    )

    __default_columns__ = ["id"]

    @classmethod
    def read_model(cls: type["BaseResourceModel"], *, depth: int = 1) -> type[BaseModel]:
        """
        Create a read model based on the current model.

        Args:
            depth: The depth of relationships to include in the read model.

        Returns:
            The read model class.
        """
        excluded_fields = []  # type: ignore
        new_annotations = {}
        fields = dict(cls.model_fields.items())

        # If depth is 0, we don't want to include any relationship representation
        if depth != 0:
            fields.update(
                {
                    relationship: cls.__annotations__[relationship]
                    for relationship in cls.__sqlmodel_relationships__.keys()
                }
            )

        for field_name, field_info in fields.items():
            # if field_name in excluded_fields and not isinstance(field_info, Mapped):
            if field_name not in excluded_fields:
                if type(field_info) == typing._GenericAlias:  # type: ignore
                    if type(field_info.__args__[0]) == BaseResourceModel:
                        type_ = field_info.__args__[0].read_model(depth=depth - 1)
                    else:
                        type_ = field_info.__args__[0]
                elif type(field_info) == UnionType:  # type: ignore
                    type_ = field_info.__args__  # type: ignore
                elif isinstance(field_info, FieldInfo):
                    type_ = field_info.annotation  # type: ignore

                new_annotations[field_name] = type_

        new_model = type(f"{cls.__name__}Read", (BaseModel,), {"__annotations__": new_annotations})
        return new_model

    @classmethod
    def create_model(cls: type["BaseResourceModel"]) -> type[BaseModel]:
        """
        Create a create model based on the current model.

        Returns:
            The create model class.
        """
        excluded_fields = cls.__default_columns__
        new_annotations = {}

        for field_name, field_info in cls.model_fields.items():
            # if field_name in excluded_fields and not isinstance(field_info, Mapped):
            if field_name not in excluded_fields:
                if type(field_info) == typing._GenericAlias:  # type: ignore
                    type_ = field_info.__args__[0]
                    continue
                elif isinstance(field_info, FieldInfo):
                    type_ = field_info.annotation
                else:
                    type_ = field_info

                new_annotations[field_name] = type_

        new_model = type(f"{cls.__name__}Create", (BaseModel,), {"__annotations__": new_annotations})
        return new_model

    @classmethod
    def update_model(cls: type["BaseResourceModel"]) -> type[BaseModel]:
        """
        Create an update model based on the current model.

        Returns:
            The update model class.
        """
        excluded_fields = cls.__default_columns__
        new_annotations = {}

        for field_name, field_info in cls.model_fields.items():
            # if field_name in excluded_fields and not isinstance(field_info, Mapped):
            if field_name not in excluded_fields:
                if type(field_info) == typing._GenericAlias:  # type: ignore
                    type_ = field_info.__args__[0]
                    continue
                elif isinstance(field_info, FieldInfo):
                    type_ = field_info.annotation
                else:
                    type_ = field_info

                new_annotations[field_name] = type_

        new_model = type(f"{cls.__name__}Update", (BaseModel,), {"__annotations__": new_annotations})
        return new_model


def create_resource_model(
    resource_config: "BlitzResourceConfig", already_created_models: dict[str, type[BaseResourceModel]]
) -> type[BaseResourceModel]:
    """
    Creates a new BaseSqlModel class based on the provided BlitzResourceConfig.

    Args:
        resource_config: The configuration object containing the information for creating the model.
        already_created_models: A dictionary containing the already created models with their corresponding table names as key.

    Returns:
        The newly created BaseSqlModel class based on the provided BlitzResourceConfig.

    This function iterates over the fields defined in the resource_config and creates the corresponding fields for the model.
    It handles different field types such as foreign keys and relationships, and sets the appropriate attributes for each field.
    """

    fields: dict[Any, Any] = {}
    for field_name, field in resource_config.fields.items():
        extra = {}
        if not isinstance(field.default, _BlitzNullValue):
            extra["default"] = field.default

        if not isinstance(field.foreign_key, _BlitzNullValue):
            extra["foreign_key"] = field.foreign_key

        if not isinstance(field.nullable, _BlitzNullValue):
            extra["nullable"] = field.nullable
        else:
            extra["nullable"] = True

        if extra["nullable"] is True and not "default" in extra:
            extra["default"] = None

        if not isinstance(field.unique, _BlitzNullValue):
            extra["unique"] = field.unique

        if field.type == AllowedBlitzFieldTypes.foreign_key:
            pass
        elif field.type == AllowedBlitzFieldTypes.relationship:
            field_info = Relationship()
            if not isinstance(field.relationship, _BlitzNullValue):
                if field.relationship not in already_created_models:
                    try:
                        field_type = eval(field.relationship)
                    except NameError:
                        field_type = f"{field.relationship}"
                    if field.relationship_list is True:
                        field_type = list[field_type]  # type: ignore
                else:
                    field_type = already_created_models[field.relationship]
            else:
                raise ValueError(f"Relationship `{field.relationship}` is missing.")
        else:
            field_info = Field(**extra)
            field_type = field.type.value

        if extra.get("nullable", False) is True:
            field_type = Optional[field_type]

        fields[field_name] = (
            field_type,
            field_info,
        )

    new_class = create_model(
        resource_config.name,
        __base__=BaseResourceModel,
        __cls_kwargs__={"table": True},
        **fields,
    )

    return new_class


def clear_metadata() -> None:
    """
    Clear the metadata of the BaseResourceModel and SQLModel classes.
    """
    SQLModel.metadata.clear()
    BaseResourceModel.metadata.clear()
