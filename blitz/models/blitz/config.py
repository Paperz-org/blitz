from pydantic import BaseModel


class BlitzAppConfig(BaseModel):
    """
    The Blitz config is the configuration for a Blitz app. It contains the name, description, and version of the app.
    """

    name: str
    description: str | None = None
    version: str
