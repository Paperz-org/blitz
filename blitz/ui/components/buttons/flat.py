from .base import BaseButton


class FlatButton(BaseButton.variant(props="flat")): # type: ignore
    """Flat button."""
