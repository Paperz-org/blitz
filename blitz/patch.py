def patch_fastapi_crudrouter() -> None:
    import fastapi_crudrouter  # type: ignore
    from fastapi_crudrouter.core._types import T, PYDANTIC_SCHEMA  # type: ignore
    from typing import Any
    from pydantic import __version__ as pydantic_version

    PYDANTIC_MAJOR_VERSION = int(pydantic_version.split(".", maxsplit=1)[0])

    def get_pk_type_patch(schema: type[PYDANTIC_SCHEMA], pk_field: str) -> Any:
        try:
            if PYDANTIC_MAJOR_VERSION >= 2:
                return schema.model_fields[pk_field].annotation
            else:
                return schema.__fields__[pk_field].type_
        except KeyError:
            return int

    from pydantic import create_model

    def schema_factory_patch(schema_cls: type[T], pk_field_name: str = "id", name: str = "Create") -> type[T]:
        """
        Is used to create a CreateSchema which does not contain pk
        """

        fields = {f.name: (f.type_, ...) for f in schema_cls.__fields__.values() if f.name != pk_field_name}
        if PYDANTIC_MAJOR_VERSION >= 2:
            # pydantic 2.x
            fields = {fk: (fv.annotation, ...) for fk, fv in schema_cls.model_fields.items() if fk != pk_field_name}
        else:
            # pydantic 1.x
            fields = {f.name: (f.type_, ...) for f in schema_cls.__fields__.values() if f.name != pk_field_name}

        name = schema_cls.__name__ + name
        schema: type[T] = create_model(__model_name=name, **fields)  # type: ignore
        return schema

    fastapi_crudrouter.core._utils.get_pk_type = get_pk_type_patch
    fastapi_crudrouter.core._utils.schema_factory = schema_factory_patch
    fastapi_crudrouter.core._base.schema_factory = schema_factory_patch
