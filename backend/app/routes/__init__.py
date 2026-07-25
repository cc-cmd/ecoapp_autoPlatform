"""Blueprint registration.

Imports all route blueprints and registers them on the Flask app.
"""


def register_blueprints(app) -> None:
    """Register all API blueprints with the Flask application.

    Blueprints are prefixed under ``/api``:

    - auth       → /api/auth
    - cases      → /api/cases
    - categories → /api/categories
    - runs       → /api/runs
    - devices    → /api/devices
    - reports    → /api/reports
    """
    from .auth import auth_bp
    from .cases import cases_bp
    from .categories import categories_bp
    from .runs import runs_bp
    from .devices import devices_bp
    from .reports import reports_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(cases_bp, url_prefix="/api/cases")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(runs_bp, url_prefix="/api/runs")
    app.register_blueprint(devices_bp, url_prefix="/api/devices")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")
