"""Request/response logging hooks.

Registers before_request and after_request handlers that produce
structured log lines for every API call.
"""

import logging
import time

from flask import g, request

logger = logging.getLogger(__name__)


def register_logging_hooks(app) -> None:
    """Attach before_request / after_request handlers that log every request.

    The before_request handler stores the request start time on ``g``.
    The after_request handler emits a single log line with method, path,
    status code, and duration in milliseconds.
    """

    @app.before_request
    def _before_request():
        # TODO: Store start time and any request-scoped context
        g.start_time = time.time()

    @app.after_request
    def _after_request(response):
        # TODO: Collect request metadata and emit structured log line
        #       e.g. logger.info("...", extra={...})
        return response

    @app.teardown_request
    def _teardown_request(_exception=None):
        # TODO: Clean up any request-scoped resources
        pass
