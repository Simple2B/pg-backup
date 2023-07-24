import os
from datetime import datetime
from functools import lru_cache
from pydantic import BaseSettings
from app.logger import log

APP_ENV = os.environ.get("APP_ENV", "development")


class BaseConfig(BaseSettings):
    """Base configuration."""

    DEBUG: bool = False
    LOG_LEVEL: int = log.INFO
    APP_NAME: str = "pg_backup"
    GITHUB_URL: str = "https://github.com/Simple2B/pg-backup"

    POSTGRES_DATABASE: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_EXTRA_OPTS: str | None
    S3_ACCESS_KEY_ID: str | None
    S3_SECRET_ACCESS_KEY: str | None
    S3_BUCKET: str | None
    S3_REGION: str | None
    S3_PATH: str = "backup"
    S3_ENDPOINT: str | None
    S3_S3V4: str = "no"
    DROP_PUBLIC: str = "yes"
    DATA_FOLDERS_TO_BACKUP: str | None
    DAYS_HISTORY: int = 30

    # Schedule
    SCHEDULE_HOUR: int | None
    SCHEDULE_MINUTE: int | None
    SCHEDULE_YEAR: int | None
    SCHEDULE_MONTH: int | None
    SCHEDULE_DAY: int | None
    SCHEDULE_WEEK: int | None
    SCHEDULE_DAY_OF_WEEK: int | None
    SCHEDULE_SECOND: int | None
    SCHEDULE_START_DATE: datetime | None
    SCHEDULE_END_DATE: datetime | None

    class Config:
        # `.env` takes priority over `project.env`
        env_file = "project.env", ".env"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    LOG_LEVEL: int = log.DEBUG
    DATABASE_URI: str

    class Config:
        fields = {
            "DATABASE_URI": {
                "env": "DEVELOP_DATABASE_URL",
            }
        }


class ProductionConfig(BaseConfig):
    """Production configuration."""

    DATABASE_URI: str

    class Config:
        fields = {
            "DATABASE_URI": {
                "env": "DATABASE_URL",
            }
        }


@lru_cache
def config(name=APP_ENV) -> DevelopmentConfig | ProductionConfig:
    CONF_MAP = dict(
        development=DevelopmentConfig(),
        production=ProductionConfig(),
    )
    configuration = CONF_MAP[name]
    configuration.ENV = name
    return configuration
