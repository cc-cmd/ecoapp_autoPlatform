"""Category management routes.

All endpoints require JWT authentication (``@jwt_required()``).

Endpoints:
  - GET  /api/categories      - Get the full category tree.
  - POST /api/categories      - Create a new category.
  - PUT  /api/categories/<id> - Rename or move a category.
  - DEL  /api/categories/<id> - Delete a category (and its children).
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/", methods=["GET"])
@categories_bp.route("", methods=["GET"])
@jwt_required()
def get_category_tree():
    """Get the full category tree as a nested list.

    Responses:
        200 → { categories: [...] }
    """
    # TODO: Implement get_category_tree
    #   - Call category_service.get_tree()
    #   - Return nested tree structure
    return jsonify({"error": "Not implemented"}), 501


@categories_bp.route("/", methods=["POST"])
@categories_bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    """Create a new category.

    Request body (JSON):
        {
            "name": "str (required)",
            "parent_id": "str (optional, null for root)",
            "sort_order": "int (optional, default 0)"
        }

    Responses:
        201 → { category: {...} }
        400 → { error: "Validation error" }
    """
    # TODO: Implement create_category
    #   - Parse and validate request JSON
    #   - Call category_service.create(data)
    #   - Return 201 with category dict
    return jsonify({"error": "Not implemented"}), 501


@categories_bp.route("/<category_id>", methods=["PUT"])
@jwt_required()
def update_category(category_id: str):
    """Update a category (rename or move).

    Request body (JSON, partial):
        {
            "name": "str (optional)",
            "parent_id": "str (optional, null for root)",
            "sort_order": "int (optional)"
        }

    Responses:
        200 → { category: {...} }
        404 → { error: "Category not found" }
    """
    # TODO: Implement update_category
    #   - Parse request JSON
    #   - Call category_service.rename() or category_service.move()
    #   - Return updated category dict
    return jsonify({"error": "Not implemented"}), 501


@categories_bp.route("/<category_id>", methods=["DELETE"])
@jwt_required()
def delete_category(category_id: str):
    """Delete a category and all its children (cascade).

    Responses:
        200 → { message: "Category deleted" }
        404 → { error: "Category not found" }
    """
    # TODO: Implement delete_category
    #   - Call category_service.delete(category_id)
    #   - Return success message
    return jsonify({"error": "Not implemented"}), 501
