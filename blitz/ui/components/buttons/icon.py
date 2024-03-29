from typing import Any
from .flat import FlatButton


class IconButton(FlatButton.variant(props="dense")):  # type: ignore
    def __init__(
        self,
        icon: str,
        on_click: Any | None = None,
        color: str = "transparent",
        icon_color: str = "secondary",
        icon_size: str = "xm",
        props: str = "",
        classes: str = "",
        **kwargs: Any,
    ):
        super().__init__(
            on_click=on_click,
            color=color,
            icon=icon,
            props=f"{props} color={icon_color} size={icon_size}",
            classes=classes,
            **kwargs,
        )
