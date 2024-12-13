import enum
import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.getcwd(), ".env")


class DBTypes(enum.StrEnum):
    SQLITE = "SQLITE"
    POSTGRESQL = "POSTGRESQL"
    MEMORY = "MEMORY"


class PostgresqlSettings(BaseSettings):
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str

    model_config = SettingsConfigDict(env_prefix="POSTGRES_", env_file=DOTENV, extra="ignore")


class Settings(BaseSettings):
    BLITZ_PORT: int = 8100
    DEFAULT_FILE: str = "blitz.json"
    BLITZ_DB_TYPE: DBTypes = DBTypes.MEMORY
    BLITZ_OPENAI_API_KEY: str = ""
    BLITZ_READ_ONLY: bool = False
    BLITZ_BASE_URL: str = "http://0.0.0.0:8100"
    POSTGRES: PostgresqlSettings | None = None

    model_config = SettingsConfigDict(env_file=DOTENV, extra="ignore")


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    if settings.BLITZ_DB_TYPE == DBTypes.POSTGRESQL:
        settings.POSTGRES = PostgresqlSettings()
    return settings
