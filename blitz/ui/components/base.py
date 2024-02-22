import time
from typing import Annotated, Any, Generic, Self, TypeVar, Protocol, cast
from blitz.ui.blitz_ui import BlitzUI, get_blitz_ui
from typing import overload
from nicegui import ui


class NiceGUIComponent(Protocol):
    def __enter__(self) -> Any:
        ...

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        ...


V = TypeVar("V", bound=NiceGUIComponent)


# Get the blitz_ui through a metaclass
class BaseComponentMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], *, reactive: bool = False) -> type:
        blitz_ui = get_blitz_ui()
        namespace["blitz_ui"] = blitz_ui
        namespace["reactive"] = reactive
        return super().__new__(cls, name, bases, namespace)


class BaseComponent(Generic[V], metaclass=BaseComponentMeta):
    def __init__(self, *args: Any, props: str = "", classes: str = "", **kwargs: Any) -> None:
        self._ng: V
        self.props: str
        self.classes: str
        self.blitz_ui: BlitzUI
        self.reactive: bool
        self.current_project = self.blitz_ui.current_project
        self.current_app = self.blitz_ui.current_app

        print("in base component", classes)
        if hasattr(self, "props"):
            self.props = f"{self.props} {props}"
        else:
            self.props = props
        if hasattr(self, "classes"):
            classes = f"{self.classes} {classes}"
        else:
            self.classes = classes

        self.blitz_ui = get_blitz_ui()
        if self.reactive:
            self.render = ui.refreshable(self.render)  # type: ignore
        self.render()

    def render(self) -> None:
        raise NotImplementedError

    def refresh(self, *args: Any, **kwargs: Any) -> None:
        if hasattr(self.render, "refresh"):
            self.render.refresh(*args, **kwargs)

    @property
    def ng(self) -> V:
        return self._ng

    @ng.setter
    def ng(self, value: V) -> None:
        self._ng = value

    @classmethod
    def variant(cls, name: str = "", *, props: str = "", classes: str = "",docstring:str="", **kwargs: Any) -> type[Self]:
        """
        Create a new type (class) based on the current component class with specified props and classes.

        :param props: The properties to be predefined in the new class.
        :param classes: The CSS classes to be predefined in the new class.
        :return: A new type (class) that is a variant of the current class with predefined props and classes.
        """
        if not name:
            new_type_name = f"{cls.__name__}_{str(time.time()).replace(".","")}"
        else:
            new_type_name = f"{name}{cls.__name__}"

        if hasattr(cls, "props"):
            props = f"{getattr(cls, 'props')} {props}"
        if hasattr(cls, "classes"):
            classes = f"{getattr(cls, 'classes')} {classes}"

        return type(
            new_type_name,
            (cls,),
            {
                "props": props,
                "classes": classes,
            },
        )
    
    def __enter__(self) -> Any | None:
        if hasattr(self.ng, "__enter__"):
            return self.ng.__enter__()
        return None

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if hasattr(self.ng, "__exit__"):
            self.ng.__exit__(exc_type, exc_value, traceback)