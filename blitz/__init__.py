import importlib.metadata

from .core import BlitzCore

__version__ = importlib.metadata.version("blitz")

__all__ = [
    "BlitzCore",
]
