import enum
import os
from functools import lru_cache

from pydantic_settings import BaseSettings

DOTENV = os.path.join(os.getcwd(), ".env")


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
    BLITZ_READ_ONLY: bool = False
    BLITZ_BASE_URL: str = "http://0.0.0.0:8100"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
