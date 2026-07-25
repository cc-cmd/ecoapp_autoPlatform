"""Report and statistics routes.

All endpoints require JWT authentication (``@jwt_required()``).

Endpoints:
  - GET /api/reports/summary  - Aggregated dashboard statistics.
  - GET /api/reports/<id>     - Detailed report for a specific batch.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_summary():
    """Get aggregated dashboard statistics.

    Returns counts and summaries for the dashboard overview.

    Query parameters:
        days (int, optional) — lookback window in days (default 7)

    Responses:
        200 → {
            "total_cases": int,
            "total_runs": int,
            "pass_rate": float,
            "automated_count": int,
            "recent_batches": [...],
            "daily_stats": [...]
        }
    """
    # TODO: Implement dashboard summary
    #   - Read optional "days" query param
    #   - Call report_service.get_summary(days)
    #   - Return aggregated statistics
    return jsonify({"error": "Not implemented"}), 501


@reports_bp.route("/<batch_id>", methods=["GET"])
@jwt_required()
def get_batch_report(batch_id: str):
    """Get a detailed report for a specific batch.

    Responses:
        200 → { batch: {...}, runs: [...], summary: {...} }
        404 → { error: "Batch not found" }
    """
    # TODO: Implement batch report
    #   - Call report_service.get_detail(batch_id)
    #   - Return batch detail with summary
    return jsonify({"error": "Not implemented"}), 501
