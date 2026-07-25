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
    error_type: str = "InternalError"

    def __init__(self, message: str | None = None, status_code: int | None = None):
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Return a JSON-serialisable error body matching the API spec:
        ``{"error": "ErrorType", "message": "human-readable description"}``.
        """
        return {"error": self.error_type, "message": self.message}


class NotFoundError(ServiceError):
    """Raised when a requested resource does not exist (404)."""

    status_code = 404
    message = "Resource not found"
    error_type = "NotFound"


class ValidationError(ServiceError):
    """Raised when request data fails validation (400)."""

    status_code = 400
    message = "Validation error"
    error_type = "ValidationError"


class ScriptValidationError(ValidationError):
    """Raised when an uploaded script fails security or syntax checks."""

    message = "Script validation failed"
    error_type = "ValidationError"


class DuplicateError(ServiceError):
    """Raised when a uniqueness constraint is violated (409)."""

    status_code = 409
    message = "Resource already exists"
    error_type = "BusinessError"


class BusinessError(ServiceError):
    """Raised for general business-rule violations (409)."""

    status_code = 409
    message = "Business rule violation"
    error_type = "BusinessError"


class InvalidTransitionError(BusinessError):
    """Raised when a state-machine transition is invalid."""

    message = "Invalid state transition"
    error_type = "BusinessError"


class DeviceNotAvailableError(BusinessError):
    """Raised when the requested device is offline or busy."""

    message = "Device not available"
    error_type = "BusinessError"


class AuthenticationError(ServiceError):
    """Raised on login / token validation failure (401)."""

    status_code = 401
    message = "Authentication failed"
    error_type = "AuthenticationError"


# ---------------------------------------------------------------------------
# Error handler registration
# ---------------------------------------------------------------------------

_service_error_classes: list[type[ServiceError]] = []


def _build_error_list() -> None:
    """Collect all ServiceError subclasses for handler registration."""
    _service_error_classes.extend([
        ServiceError,
        NotFoundError,
        ValidationError,
        ScriptValidationError,
        DuplicateError,
        BusinessError,
        InvalidTransitionError,
        DeviceNotAvailableError,
        AuthenticationError,
    ])


def register_error_handlers(app) -> None:
    """Register JSON error handlers on the Flask application.

    Catches:
      - All ServiceError subclasses → JSON with configured status code.
      - 404 (route not found)       → JSON instead of HTML.
      - 405 (method not allowed)    → JSON.
      - 500 (unhandled exception)   → JSON with generic message.
    """
    _build_error_list()

    # ---- ServiceError subclasses ----
    for exc_cls in _service_error_classes:

        def _make_handler(cls: type[ServiceError]):
            def handler(error: ServiceError):
                return jsonify(error.to_dict()), error.status_code

            handler.__name__ = f"handle_{cls.__name__}"
            return handler

        app.errorhandler(exc_cls)(_make_handler(exc_cls))

    # ---- Generic HTTP errors ----

    @app.errorhandler(404)
    def _handle_404(_error):
        return jsonify({"error": "NotFound", "message": "Not found"}), 404

    @app.errorhandler(405)
    def _handle_405(_error):
        return jsonify({"error": "MethodNotAllowed", "message": "Method not allowed"}), 405

    @app.errorhandler(500)
    def _handle_500(_error):
        return (
            jsonify({"error": "InternalError", "message": "Internal server error"}),
            500,
        )
