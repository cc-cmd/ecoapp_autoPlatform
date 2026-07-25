"""Run execution and management routes.

All endpoints require JWT authentication (``@jwt_required()``).

Endpoints:
  - GET  /api/runs                           - List run batches.
  - POST /api/runs                           - Trigger a new batch.
  - GET  /api/runs/<id>                      - Batch detail (with runs).
  - POST /api/runs/<id>/cancel               - Cancel an entire batch.
  - POST /api/runs/<id>/runs/<run_id>/cancel  - Cancel a single run.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

runs_bp = Blueprint("runs", __name__)


@runs_bp.route("/", methods=["GET"])
@runs_bp.route("", methods=["GET"])
@jwt_required()
def list_batches():
    """List run batches with pagination.

    Query parameters:
        page (int, default 1)
        size (int, default 20)
        status (str, optional) — filter by batch status

    Responses:
        200 → { items: [...], total, page, size }
    """
    # TODO: Implement batch listing
    #   - Read query params
    #   - Call run_service.list_batches(...)
    #   - Return paginated response
    return jsonify({"error": "Not implemented"}), 501


@runs_bp.route("/", methods=["POST"])
@runs_bp.route("", methods=["POST"])
@jwt_required()
def trigger_batch():
    """Trigger a new execution batch.

    Request body (JSON):
        {
            "name": "str (optional, auto-generated if omitted)",
            "case_ids": ["str", ...] (required, at least 1),
            "device_id": "str (optional, auto-allocate if omitted)"
        }

    Responses:
        201 → { batch: {...}, runs: [...] }
        400 → { error: "Validation error" }
    """
    # TODO: Implement batch trigger
    #   - Parse and validate request JSON
    #   - Extract current user id (get_jwt_identity())
    #   - Call run_service.trigger(...)
    #   - Return 201 with batch and runs
    return jsonify({"error": "Not implemented"}), 501


@runs_bp.route("/<batch_id>", methods=["GET"])
@jwt_required()
def get_batch_detail(batch_id: str):
    """Get batch detail including all child test runs.

    Responses:
        200 → { batch: {...}, runs: [...] }
        404 → { error: "Batch not found" }
    """
    # TODO: Implement batch detail
    #   - Call run_service.get_batch_detail(batch_id)
    #   - Return batch + runs
    return jsonify({"error": "Not implemented"}), 501


@runs_bp.route("/<batch_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_batch(batch_id: str):
    """Cancel an entire batch (only allowed for queued / running).

    Cancelling a running batch will attempt to halt any in-progress run.

    Responses:
        200 → { message: "Batch cancelled" }
        400 → { error: "Batch is already in a terminal state" }
        404 → { error: "Batch not found" }
    """
    # TODO: Implement batch cancellation
    #   - Call run_service.cancel_batch(batch_id)
    #   - Return success message
    return jsonify({"error": "Not implemented"}), 501


@runs_bp.route("/<batch_id>/runs/<run_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_run(batch_id: str, run_id: str):
    """Cancel a single run within a batch.

    Only allowed if the run is currently queued or running.

    Responses:
        200 → { message: "Run cancelled" }
        400 → { error: "Run is already in a terminal state" }
        404 → { error: "Run not found" }
    """
    # TODO: Implement single run cancellation
    #   - Call run_service.cancel_run(batch_id, run_id)
    #   - Return success message
    return jsonify({"error": "Not implemented"}), 501
