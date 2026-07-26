"""Application configuration classes.

Uses environment variables with sensible defaults.
Supports three environments: development, testing, production.
"""

import os
from datetime import timedelta


class BaseConfig:
    """Base configuration shared across all environments."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/auto_project"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_size": 10,
        "pool_recycle": 300,
    }

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "86400"))
    )
    JWT_ERROR_MESSAGE_KEY = "error"
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    # Appium
    APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
    APPIUM_PORT = int(os.getenv("APPIUM_PORT", "4723"))

    # Scheduler
    SCHEDULER_HEARTBEAT_INTERVAL = int(
        os.getenv("SCHEDULER_HEARTBEAT_INTERVAL", "30")
    )
    SCHEDULER_QUEUE_INTERVAL = int(os.getenv("SCHEDULER_QUEUE_INTERVAL", "3"))

    # Upload
    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"),
    )
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = os.getenv("LOG_DIR", "logs")
    LOG_FILE = "app.log"
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 10


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""

    DEBUG = True
    LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")


class TestingConfig(BaseConfig):
    """Testing environment configuration.

    Uses an in-memory SQLite database for fast test isolation.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)
    LOG_LEVEL = "WARNING"


class ProductionConfig(BaseConfig):
    """Production environment configuration."""

    DEBUG = False
    SQLALCHEMY_ECHO = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
