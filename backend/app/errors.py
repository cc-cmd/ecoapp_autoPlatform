"""Custom exception hierarchy and Flask error handler registration.

All service-level errors inherit from ServiceError so callers can catch
a single base type when desired. Each subclass maps to an HTTP status
code returned via register_error_handlers().
"""

from flask import jsonify


# ---------------------------------------------------------------------------
# Exception hierarchy
# ---------------------------------------------------------------------------


class ServiceError(Exception):
    """Base exception for all service-layer errors."""

    status_code: int = 500
    message: str = "Internal server error"

    def __init__(self, message: str | None = None, status_code: int | None = None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Return a JSON-serialisable error body."""
        return {"error": self.message, "status_code": self.status_code}


class NotFoundError(ServiceError):
    """Raised when a requested resource does not exist (404)."""

    status_code = 404
    message = "Resource not found"


class ValidationError(ServiceError):
    """Raised when request data fails validation (400)."""

    status_code = 400
    message = "Validation error"


class ScriptValidationError(ValidationError):
    """Raised when an uploaded script fails security or syntax checks."""

    message = "Script validation failed"


class DuplicateError(ServiceError):
    """Raised when a uniqueness constraint is violated."""

    status_code = 409
    message = "Resource already exists"


class BusinessError(ServiceError):
    """Raised for general business-rule violations (409)."""

    status_code = 409
    message = "Business rule violation"


class InvalidTransitionError(BusinessError):
    """Raised when a state-machine transition is invalid."""

    message = "Invalid state transition"


class DeviceNotAvailableError(BusinessError):
    """Raised when the requested device is offline or busy."""

    message = "Device not available"


class AuthenticationError(ServiceError):
    """Raised on login / token validation failure (401)."""

    status_code = 401
    message = "Authentication failed"


# ---------------------------------------------------------------------------
# Error handler registration
# ---------------------------------------------------------------------------

_service_error_map: dict[type[ServiceError], tuple[int, str]] = {}


def _build_error_map() -> None:
    """Build a lookup from exception type to (status_code, default_message)."""
    for cls in (
        ServiceError,
        NotFoundError,
        ValidationError,
        ScriptValidationError,
        DuplicateError,
        BusinessError,
        InvalidTransitionError,
        DeviceNotAvailableError,
        AuthenticationError,
    ):
        _service_error_map[cls] = (cls.status_code, cls.message)


def register_error_handlers(app) -> None:
    """Register JSON error handlers on the Flask application.

    Catches:
      - All ServiceError subclasses → JSON with configured status code.
      - 404 (route not found)       → JSON instead of HTML.
      - 405 (method not allowed)    → JSON.
      - 500 (unhandled exception)   → JSON with generic message.
    """
    _build_error_map()

    # ---- ServiceError subclasses ----
    for exc_cls in _service_error_map:

        def _make_handler(cls: type[ServiceError]):
            def handler(error: ServiceError):
                return jsonify(error.to_dict()), error.status_code

            handler.__name__ = f"handle_{cls.__name__}"
            return handler

        app.errorhandler(exc_cls)(_make_handler(exc_cls))

    # ---- Generic HTTP errors ----

    @app.errorhandler(404)
    def _handle_404(_error):
        return jsonify({"error": "Not found", "status_code": 404}), 404

    @app.errorhandler(405)
    def _handle_405(_error):
        return jsonify({"error": "Method not allowed", "status_code": 405}), 405

    @app.errorhandler(500)
    def _handle_500(_error):
        return (
            jsonify({"error": "Internal server error", "status_code": 500}),
            500,
        )
