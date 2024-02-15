import base64
import json
from typing import Any
import zlib

from sqlalchemy import Column, MetaData, Table


def determine_relationship_type(column: Column[Any], tables: dict[str, Table]) -> str:
    """
    Determine the relationship type based on a foreign key column.
    Args:
        column: The foreign key column which contains information about both
                the referencing and referenced table.
        tables: A dictionary of table names to Table objects.
    Returns:
        The relationship type as a string.
        #TODO can be improved with an enum
    Raises:
        Exception: If the relationship type cannot be determined.
    """
    if not column.foreign_keys:
        raise Exception(f"{column.table.name}.{column.name} does not have a foreign key reference.")

    foreign_key = list(column.foreign_keys)[0]

    current_side = "o|" if column.nullable else "||"
    referenced_table = foreign_key.column.table

    for _, other_table in tables.items():
        for other_column in other_table.columns:
            if other_column.foreign_keys:
                if list(other_column.foreign_keys)[0].column.table.name == referenced_table.name:
                    if other_column.unique:
                        return f"|| -- {current_side}"
                    other_side = "}o" if other_column.nullable else "}|"
                    return f"{other_side} -- {current_side}"

    raise Exception(f"Could not determine relationship type for {column.table.name}.{column.name}")


def generate_mermaid_erd(metadata: MetaData) -> str:
    """
    Generate Mermaid ERD from SQLAlchemy Metadata.
    #TODO improve documentation
    """
    erd = ["erDiagram"]

    tables = metadata.tables

    for table_name, table in tables.items():
        columns = []
        for col in table.columns:
            col_desc = f"{col.name} {col.type}"
            if col.primary_key:
                col_desc += " PK"
            if col.foreign_keys:
                col_desc += " FK"
            columns.append(col_desc)
        columns_definition = "\n    ".join(columns)
        erd.append(f"  {table_name} {{\n    {columns_definition}\n  }}")

    visited_relations = set()
    for table_name, table in tables.items():
        for column in table.columns:
            if column.foreign_keys:
                referenced_table = list(column.foreign_keys)[0].column.table.name

                relation = determine_relationship_type(column, tables)
                relation_key = tuple(sorted([table_name, referenced_table]))

                if relation and relation_key not in visited_relations:
                    erd.append(f'  {table_name} {relation} {referenced_table}: " "')
                    visited_relations.add(relation_key)

    return "\n".join(erd)


def mermaid_serialize(erd: str) -> str:
    """
    Based on the mermaid-live-editor implementation
    For data format:
    https://github.com/mermaid-js/mermaid-live-editor/blob/414c5bb59b162dae0a2ecc775828069a50725ee8/src/lib/types.d.ts#L21
    For data serialization:
    https://github.com/mermaid-js/mermaid-live-editor/blob/414c5bb59b162dae0a2ecc775828069a50725ee8/src/lib/util/serde.ts#L19
    """
    data = json.dumps(
        {
            "code": erd,
            "mermaid": '{ "theme": "dark" }',
            "autoSync": False,
            "updateDiagram": False,
            "panZoom": True,
            "pan": {"x": 0, "y": 0},
            "zoom": 1,
        }
    )
    compressed = zlib.compress(data.encode("utf-8"), level=9)
    return base64.urlsafe_b64encode(compressed).decode("utf-8")


def _mermaid_deserialize(state: str) -> dict[str, Any]:
    """
    For development purpose if you want to deserialize the data.
    """
    missing_padding = len(state) % 4
    if missing_padding:
        state += "=" * (4 - missing_padding)
    data = base64.urlsafe_b64decode(state)
    return dict(json.loads(zlib.decompress(data).decode("utf-8")))
