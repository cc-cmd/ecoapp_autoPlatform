"""Structured JSON logging and request hooks.

Configures dual-output logging (stdout + rotating file) with JSON format,
then registers before_request / after_request / teardown_request handlers
that produce a log line per HTTP request with a unique request_id for
end-to-end tracing.
"""

import json
import logging
import logging.handlers
import os
import sys
import time
import traceback
import uuid
from datetime import datetime, timezone

from flask import g, request

_logging_initialized = False


class JsonFormatter(logging.Formatter):
    """Custom formatter that emits each log record as a single JSON line.

    Output includes a fixed set of fields (time, level, module, message)
    plus optional request-scoped context (request_id, path, method,
    status_code, duration_ms, ip) when those keys are present in the
    record's ``extra`` dict.

    When the record carries exception info (``logger.exception()`` or
    ``exc_info=True``), an ``exception`` object with type, message, and
    traceback is appended.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict = {
            "time": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }

        # Request-scoped context (only present during HTTP request handling)
        for key in (
            "request_id",
            "path",
            "method",
            "status_code",
            "duration_ms",
            "ip",
        ):
            value = record.__dict__.get(key)
            if value is not None:
                log_entry[key] = value

        # Exception info
        if record.exc_info and record.exc_info[0] is not None:
            exc_type, exc_value, _exc_tb = record.exc_info
            log_entry["exception"] = {
                "type": exc_type.__name__,
                "message": str(exc_value),
                "traceback": traceback.format_exception(
                    exc_type, exc_value, _exc_tb
                ),
            }

        return json.dumps(log_entry, ensure_ascii=False)


def init_logging(app) -> None:
    """Initialise structured JSON logging and register request hooks.

    Must be called **after** ``app.config`` is loaded and **before** any
    extensions so that subsequent initialisation errors are captured.

    Idempotent — subsequent calls are no-ops to prevent handler
    duplication and file-descriptor leaks.

    - Creates the log directory (``LOG_DIR``) relative to ``backend/``.
    - Adds a ``StreamHandler`` (stdout) and a ``RotatingFileHandler``
      (10 MB × 10 backups), both using :class:`JsonFormatter`.
    - Redirects Werkzeug's access log through the same handlers.
    - Quietens SQLAlchemy engine logging to WARNING unless LOG_LEVEL is DEBUG.
    - Registers ``before_request``, ``after_request``, and
      ``teardown_request`` hooks.
    """
    global _logging_initialized

    if _logging_initialized:
        return
    _logging_initialized = True

    # Resolve log directory relative to backend/
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(backend_dir, app.config["LOG_DIR"])
    os.makedirs(log_dir, exist_ok=True)

    # Per-session log file: yyyy-mm-dd-<8-char-uuid>.log
    # A new file is created on every startup so logs from different
    # runs never mix in a single file.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    session_id = uuid.uuid4().hex[:8]
    log_filename = f"{today}-{session_id}.log"
    log_file = os.path.join(log_dir, log_filename)

    log_level = app.config["LOG_LEVEL"]
    if not isinstance(log_level, str):
        log_level = "INFO"

    formatter = JsonFormatter()

    # ---- Handlers ----
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    # Discard any default / previously configured handlers
    root_logger.handlers.clear()

    # Console → stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File → rotating
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=app.config["LOG_MAX_BYTES"],
        backupCount=app.config["LOG_BACKUP_COUNT"],
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # ---- Third-party logger tuning ----
    # Suppress Werkzeug's built-in access log — we produce our own
    # structured request log in _after_request.  Only let WARNING+
    # through (real issues, not routine HTTP access lines).
    logging.getLogger("werkzeug").handlers.clear()
    logging.getLogger("werkzeug").setLevel(logging.WARNING)

    # Keep SQLAlchemy quiet unless we are in DEBUG mode
    sqlalchemy_level = "INFO" if log_level == "DEBUG" else "WARNING"
    logging.getLogger("sqlalchemy.engine").setLevel(sqlalchemy_level)

    # Suppress noisy third-party startup chatter
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("tzlocal").setLevel(logging.WARNING)

    # Flask's debug mode adds its own plain-text StreamHandler the first
    # time app.logger is accessed.  Access it now to trigger that, then
    # remove the handler so every log line uses our JSON formatter only.
    _ = app.logger  # eager-init Flask's internal _logger
    app.logger.handlers.clear()
    app.logger.info("Logging initialised — level=%s, file=%s", log_level, log_filename)

    # ---- Request hooks ----
    @app.before_request
    def _before_request():
        g.start_time = time.monotonic()
        g.request_id = uuid.uuid4().hex[:8]

    @app.after_request
    def _after_request(response):
        duration_ms = (time.monotonic() - g.get("start_time", time.monotonic())) * 1000

        app.logger.info(
            "%s %s %s",
            request.method,
            request.path,
            response.status_code,
            extra={
                "request_id": g.get("request_id", "-"),
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 1),
                "ip": request.remote_addr,
            },
        )
        return response

    @app.teardown_request
    def _teardown_request(_exception=None):
        if _exception is not None:
            # Pass the actual exception object rather than exc_info=True
            # because Flask may have already cleared sys.exc_info() by
            # the time teardown hooks fire.
            app.logger.error(
                "Unhandled exception during request: %s %s",
                request.method,
                request.path,
                exc_info=_exception,
                extra={
                    "request_id": g.get("request_id", "-"),
                    "method": request.method,
                    "path": request.path,
                    "ip": request.remote_addr,
                },
            )
