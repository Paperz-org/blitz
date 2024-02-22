from typing import Any, Self
from blitz.ui.components.base import BaseComponent
from nicegui import ui

class BaseRow(BaseComponent[ui.row]):
    def __init__(self, wrap: bool = True,props: str = "", classes: str = "") -> None:
        self.wrap = wrap
        print("--->", "in init", classes)
        super().__init__(props=props, classes=classes)
    
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        instance = super().__new__(cls)
        instance.__init__(*args, **kwargs)
        print("--------->", instance.classes)
        for parent in cls.mro():
            if hasattr(parent, "classes"):
                instance.classes = parent.classes
        return instance
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == "classes" and hasattr(self, "classes"):
            print("!!!!!!!!",__value)
            if  __value in self.classes:
                return 
            __value = f"{self.classes} {__value}"
        return super().__setattr__(__name, __value)
    
    def render(self) -> None:
        print(self.classes)
        self.ng = ui.row(wrap=self.wrap).props(self.props).classes(self.classes)



class WFullRow(BaseRow.variant(classes="w-full")): # type: ignore
    """Row with w-full class."""
    ...

class ContentCenterRow(BaseRow.variant(classes="content-center")): # type: ignore
    """Row with content-center class."""
    ...

class ItemsCenterRow(BaseRow.variant(classes="items-center")): # type: ignore
    """Row with items-center class."""
    ...

class WFullItemsCenter(WFullRow, ItemsCenterRow):
    """Row with w-full and items-center classes."""
    ...

class WFullContentCenterRow(WFullRow, ContentCenterRow):
    """Row with w-full and content-center classes."""
    ...

class ItemsCenterContentCenterRow(ItemsCenterRow, ContentCenterRow):
    """Row with items-center and content-center classes."""
    ...