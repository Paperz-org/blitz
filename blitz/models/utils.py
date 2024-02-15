import enum
from typing import Any


class ContainsEnum(enum.EnumMeta):
    """
    Metaclass for Enums that provides a __contains__ method.

    This metaclass allows checking if a value is a valid member of the Enum by using the 'in' operator.

    Example:
        >>> class MyEnum(Enum, metaclass=ContainsEnum):
        ...    VALUE1 = 'value1'
        ...    VALUE2 = 'value2'

        >>> print('value1' in MyEnum)  # Output: True
        >>> print('value3' in MyEnum)  # Output: False

    """

    def __new__(mcs, name: str, bases: tuple[Any], classdict: Any) -> "ContainsEnum":
        return super().__new__(mcs, name, bases, classdict)

    def __contains__(cls, item: Any) -> bool:
        try:
            instance: enum.Enum = cls(item)
            if isinstance(instance.value, enum.auto):
                return False
        except ValueError:
            return False
        else:
            return True
