import enum
from functools import lru_cache
import os

from pydantic_settings import BaseSettings

DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class DBTypes(enum.StrEnum):
    SQLITE = "SQLITE"
    MEMORY = "MEMORY"


class Settings(BaseSettings):
    class Config:
        env_file = DOTENV
        extra = "ignore"

    BLITZ_PORT: int = 8100
    DEFAULT_FILE: str = "blitz.json"
    BLITZ_DB_TYPE: DBTypes = DBTypes.SQLITE
    BLITZ_OPENAI_API_KEY: str = ""


@lru_cache()
def get_settings() -> Settings:
    return Settings()
