"""Authentication routes.

Public endpoints (no JWT required):
  - POST /api/auth/register  - Create a new user account.
  - POST /api/auth/login     - Authenticate and receive a JWT access token.
"""

import logging

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.services.auth_service import AuthService
from app.errors import (
    ValidationError,
    DuplicateError,
    AuthenticationError,
)

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)


def _get_auth_service() -> AuthService:
    """Create an AuthService instance bound to the current DB session."""
    return AuthService(db.session)


def _parse_json_body() -> dict:
    """Parse and validate the request JSON body.

    Returns:
        Parsed JSON dict.

    Raises:
        ValidationError: If Content-Type is wrong or body is not valid JSON.
    """
    if not request.is_json:
        raise ValidationError("请求体必须为 JSON 格式")
    data = request.get_json(silent=True)
    if data is None:
        raise ValidationError("请求体不能为空")
    return data


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Request body (JSON):
        {
            "username": "str (3-64 chars)",
            "password": "str (at least 8 chars, must contain letter + digit)"
        }

    Responses:
        201 → { "user": {"id": "...", "username": "...", "created_at": "..."} }
        400 → { "error": "ValidationError", "message": "..." }
        409 → { "error": "BusinessError", "message": "..." }

        Note: Registration does NOT return a JWT token.
        The user must explicitly log in afterwards.
    """
    data = _parse_json_body()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise ValidationError("用户名和密码为必填项")

    auth_service = _get_auth_service()
    user = auth_service.register(username, password)
    db.session.commit()

    logger.info("User registered: %s (%s)", user.username, user.id)

    return jsonify({"user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Authenticate a user and return a JWT token.

    Request body (JSON):
        {
            "username": "str",
            "password": "str"
        }

    Responses:
        200 → { "token": "...", "user": {"id": "...", "username": "..."} }
        400 → { "error": "ValidationError", "message": "..." }
        401 → { "error": "AuthenticationError", "message": "..." }
    """
    data = _parse_json_body()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        raise ValidationError("用户名和密码为必填项")

    auth_service = _get_auth_service()
    user = auth_service.login(username, password)

    # Generate JWT at the route layer (service stays framework-agnostic)
    access_token = create_access_token(identity=str(user.id))

    logger.info("User logged in: %s (%s)", user.username, user.id)

    return jsonify({
        "token": access_token,
        "user": {
            "id": str(user.id),
            "username": user.username,
        },
    }), 200
