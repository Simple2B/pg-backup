import os
from datetime import datetime
from functools import lru_cache
from pydantic_settings import BaseSettings
from .logger import log

APP_ENV = os.environ.get("APP_ENV", "development")


class BaseConfig(BaseSettings):
    """Base configuration."""

    ENV: str = APP_ENV
    DEBUG: bool = False
    LOG_LEVEL: int = log.INFO
    APP_NAME: str = "pg_backup"
    GITHUB_URL: str = "https://github.com/Simple2B/pg-backup"

    POSTGRES_DATABASE: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_EXTRA_OPTS: str = ""
    LOCAL_DB_PORT: int = 5432
    S3_ACCESS_KEY_ID: str
    S3_SECRET_ACCESS_KEY: str
    S3_BUCKET: str
    S3_REGION: str
    S3_PREFIX: str = "backup"
    S3_ENDPOINT: str | None
    S3_S3V4: str = "no"
    DROP_PUBLIC: str = "yes"
    DATA_FOLDERS_TO_BACKUP: str
    DAYS_HISTORY: int = 30

    # Schedule
    SCHEDULE_HOUR: int = 0
    SCHEDULE_MINUTE: int = 0
    SCHEDULE_YEAR: int | str = "*"
    SCHEDULE_MONTH: int | str = "*"
    SCHEDULE_DAY: int | str = "*"
    SCHEDULE_WEEK: int | str = "*"
    SCHEDULE_DAY_OF_WEEK: int | str = "*"
    SCHEDULE_SECOND: int = 0
    SCHEDULE_START_DATE: datetime | None = None
    SCHEDULE_END_DATE: datetime | None = None

    class Config:
        # `.env` takes priority over `project.env`
        env_file = "project.env", ".env"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    LOG_LEVEL: int = log.DEBUG


class ProductionConfig(BaseConfig):
    """Production configuration."""

    LOG_LEVEL: int = log.INFO


@lru_cache
def config(name=APP_ENV) -> DevelopmentConfig | ProductionConfig:
    CONF_MAP = dict(
        development=DevelopmentConfig,
        production=ProductionConfig,
    )
    configuration = CONF_MAP[name]()
    configuration.ENV = name
    return configuration
