"""Alembic environment configuration.

Loads Flask application configuration to determine the database URL
and imports all models so that Alembic can auto-generate migrations.
"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv

# -----------------------------------------------------------
# Load .env file (so DATABASE_URL is available when Alembic
# is run outside the Flask CLI context, e.g. "flask db upgrade").
# -----------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------
# Ensure the backend package is on sys.path so that ``from app``
# imports work correctly when alembic is run from the project
# root or from the migrations/ directory.
# -----------------------------------------------------------
_backend_dir = os.path.join(os.path.dirname(__file__), "..")
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# -----------------------------------------------------------
# Alembic Config object
# -----------------------------------------------------------
config = context.config

# -----------------------------------------------------------
# Logging
# -----------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------------------------------------
# Set sqlalchemy.url from Flask app config
# -----------------------------------------------------------
from app import create_app

_flask_app = create_app(os.getenv("FLASK_ENV", "development"))
with _flask_app.app_context():
    config.set_main_option("sqlalchemy.url", _flask_app.config["SQLALCHEMY_DATABASE_URI"])

# -----------------------------------------------------------
# Import all models so Alembic can detect table definitions
# -----------------------------------------------------------
from app.models import User, Category, TestCase, Device, RunGroup, TestRun  # noqa: E402, F401
from app.extensions import db

target_metadata = db.metadata

# -----------------------------------------------------------
# Migration functions
# -----------------------------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Generates SQL scripts without connecting to a database.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode, connecting to the database."""
    from sqlalchemy import engine_from_config, pool

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
