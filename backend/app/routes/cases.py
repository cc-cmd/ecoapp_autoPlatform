"""Test case management routes.

All endpoints require JWT authentication (``@jwt_required()``).

Endpoints:
  - GET    /api/cases                - List / search test cases.
  - POST   /api/cases                - Create a new test case.
  - GET    /api/cases/<id>           - Get test case detail.
  - PUT    /api/cases/<id>           - Update a test case.
  - DELETE /api/cases/<id>           - Delete a test case.
  - POST   /api/cases/<id>/script    - Upload a Python script.
  - GET    /api/cases/<id>/script    - Download / view the script content.
  - GET    /api/cases/<id>/runs      - List execution history for a case.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

cases_bp = Blueprint("cases", __name__)


@cases_bp.route("/", methods=["GET"])
@cases_bp.route("", methods=["GET"])
@jwt_required()
def list_cases():
    """List test cases with optional filtering and pagination.

    Query parameters:
        page (int, default 1)
        size (int, default 20)
        search (str, optional) — fuzzy search on name
        category_id (str, optional)
        priority (str, optional)
        is_automated (bool, optional)

    Responses:
        200 → { items: [...], total, page, size }
    """
    # TODO: Implement case listing
    #   - Read query params with defaults
    #   - Call case_service.list_cases(...)
    #   - Return paginated response
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/", methods=["POST"])
@cases_bp.route("", methods=["POST"])
@jwt_required()
def create_case():
    """Create a new test case.

    Request body (JSON):
        {
            "name": "str (required)",
            "priority": "P0|P1|P2|P3 (default P2)",
            "steps": "str (optional)",
            "category_id": "str (optional)"
        }

    Responses:
        201 → { case: {...} }
        400 → { error: "Validation error" }
    """
    # TODO: Implement case creation
    #   - Parse and validate request JSON
    #   - Extract current user id from JWT (get_jwt_identity())
    #   - Call case_service.create_case(...)
    #   - Return 201 with case dict
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/<case_id>", methods=["GET"])
@jwt_required()
def get_case(case_id: str):
    """Get detailed information for a single test case.

    Responses:
        200 → { case: {...} }
        404 → { error: "Case not found" }
    """
    # TODO: Implement get_case
    #   - Call case_service.get_case(case_id)
    #   - Return case dict
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/<case_id>", methods=["PUT"])
@jwt_required()
def update_case(case_id: str):
    """Update an existing test case.

    Request body (JSON, partial updates supported):
        {
            "name": "str (optional)",
            "priority": "str (optional)",
            "steps": "str (optional)",
            "category_id": "str (optional)"
        }

    Responses:
        200 → { case: {...} }
        400 → { error: "Validation error" }
        404 → { error: "Case not found" }
    """
    # TODO: Implement case update
    #   - Parse request JSON
    #   - Call case_service.update_case(case_id, data)
    #   - Return updated case dict
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/<case_id>", methods=["DELETE"])
@jwt_required()
def delete_case(case_id: str):
    """Delete a test case and its stored script.

    Responses:
        200 → { message: "Case deleted" }
        404 → { error: "Case not found" }
    """
    # TODO: Implement case deletion
    #   - Call case_service.delete_case(case_id)
    #   - Return success message
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/<case_id>/script", methods=["POST"])
@jwt_required()
def upload_script(case_id: str):
    """Upload a Python script for the test case.

    Request: multipart/form-data with field "file".
    File must be a valid .py file (validated by AST security check).

    Responses:
        200 → { message: "Script uploaded", script_path: "..." }
        400 → { error: "Validation error" }
        404 → { error: "Case not found" }
    """
    # TODO: Implement script upload
    #   - Get file from request.files
    #   - Call case_service.upload_script(case_id, file)
    #   - Return success with script path
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/<case_id>/script", methods=["GET"])
@jwt_required()
def get_script(case_id: str):
    """Get the content of the uploaded script for a test case.

    Responses:
        200 → Script file content (text/plain)
        404 → { error: "Case not found" or "No script uploaded" }
    """
    # TODO: Implement get_script
    #   - Call case_service.get_script_path(case_id)
    #   - Read and return script file content
    return jsonify({"error": "Not implemented"}), 501


@cases_bp.route("/<case_id>/runs", methods=["GET"])
@jwt_required()
def get_case_runs(case_id: str):
    """List execution history for a specific test case.

    Query parameters:
        page (int, default 1)
        size (int, default 20)

    Responses:
        200 → { items: [...], total, page, size }
        404 → { error: "Case not found" }
    """
    # TODO: Implement case execution history
    #   - Read pagination params
    #   - Call case_service.get_execution_history(case_id, page, size)
    #   - Return paginated response
    return jsonify({"error": "Not implemented"}), 501
