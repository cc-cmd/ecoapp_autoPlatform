"""Flask application factory (create_app).

Initialises extensions, registers blueprints, error handlers,
logging hooks, and the background scheduler.
"""

import os

from flask import Flask
from flask_cors import CORS

from .config import config
from .extensions import db, jwt, migrate


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Steps:
        1. Create Flask instance.
        2. Load configuration from ``config`` dict.
        3. Initialise extensions (db, jwt, migrate, cors).
        4. Register error handlers (errors.py).
        5. Register logging hooks (logging_config.py).
        6. Register blueprints (routes/__init__.py).
        7. Initialise background scheduler (scheduler.py).
        8. Set up teardown cleanup.

    Args:
        config_name: One of "development", "testing", "production".
                     Defaults to FLASK_ENV env var or "development".

    Returns:
        Configured Flask application instance.
    """
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config["development"]))

    # Return Chinese characters as-is in JSON responses (not \uXXXX)
    app.json.ensure_ascii = False

    # ------------------------------------------------------------------
    # Initialise logging (must come early so all subsequent code can log)
    # ------------------------------------------------------------------
    from .logging_config import init_logging

    init_logging(app)

    # ------------------------------------------------------------------
    # Initialise extensions
    # ------------------------------------------------------------------
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Enable CORS for development
    if config_name == "development":
        CORS(app)

    # ------------------------------------------------------------------
    # Register error handlers
    # ------------------------------------------------------------------
    from .errors import register_error_handlers

    register_error_handlers(app)

    # ------------------------------------------------------------------
    # Register blueprints
    # ------------------------------------------------------------------
    from .routes import register_blueprints

    register_blueprints(app)

    # ------------------------------------------------------------------
    # Initialise scheduler (skip in testing)
    # ------------------------------------------------------------------
    if config_name != "testing":
        from .scheduler import init_scheduler

        init_scheduler(app)

    # ------------------------------------------------------------------
    # Teardown cleanup
    # ------------------------------------------------------------------
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        """Remove the database session after each request."""
        db.session.remove()

    return app
