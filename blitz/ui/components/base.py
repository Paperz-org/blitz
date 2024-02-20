from typing import Any, Self, Tuple, TypeVar
from blitz.ui.blitz_ui import get_blitz_ui

T = TypeVar("T", bound="BaseComponent")


class BaseComponent:
    def __init__(self, *args: Any, props: str = "", classes: str = "", **kwargs: Any) -> None:
        self.props: str
        self.classes: str

        if hasattr(self, "props"):
            self.props = f"{self.props} {props}"
        else:
            self.props = props
        if hasattr(self, "classes"):
            classes = f"{self.classes} {classes}"
        else:
            self.classes = classes

        self.blitz_ui = get_blitz_ui()
        self.render()

    def render(self) -> None:
        raise NotImplementedError

    @classmethod
    def variant(cls, name: str, *, props: str = "", classes: str = "", **kwargs: Any) -> type[Self]:
        """
        Create a new type (class) based on the current component class with specified props and classes.

        :param props: The properties to be predefined in the new class.
        :param classes: The CSS classes to be predefined in the new class.
        :return: A new type (class) that is a variant of the current class with predefined props and classes.
        """

        if hasattr(cls, "props"):
            props = f"{getattr(cls, 'props')} {props}"
        if hasattr(cls, "classes"):
            classes = f"{getattr(cls, 'classes')} {classes}"

        return type(
            f"{name}{cls.__name__}",
            (cls,),
            {
                "props": props,
                "classes": classes,
            },
        )
