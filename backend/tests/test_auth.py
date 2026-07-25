"""Authentication endpoint tests.

Tests are grouped into two categories:
  1. Registration (POST /api/auth/register)
  2. Login (POST /api/auth/login)

All tests run against the real PostgreSQL database.  Test data is
rolled back via transaction isolation (see conftest.py).
"""

import uuid

import pytest
from flask.testing import FlaskClient


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _unique_username() -> str:
    """Generate a unique username for test isolation."""
    return f"test_{uuid.uuid4().hex[:12]}"


# ---------------------------------------------------------------------------
# Registration tests
# ---------------------------------------------------------------------------


class TestRegister:
    """Tests for POST /api/auth/register."""

    def test_register_success(self, client: FlaskClient):
        """Register with valid credentials returns 201 and user info (no token)."""
        resp = client.post(
            "/api/auth/register",
            json={"username": _unique_username(), "password": "Pass1234"},
        )
        assert resp.status_code == 201, resp.get_json()
        data = resp.get_json()
        assert "user" in data
        assert "token" not in data  # Registration does NOT return a token
        assert "id" in data["user"]
        assert data["user"]["username"] is not None

    def test_register_duplicate_username(self, client: FlaskClient):
        """Registering with an existing username returns 409."""
        username = _unique_username()
        # First registration
        resp = client.post(
            "/api/auth/register",
            json={"username": username, "password": "Pass1234"},
        )
        assert resp.status_code == 201

        # Duplicate registration
        resp = client.post(
            "/api/auth/register",
            json={"username": username, "password": "Pass1234"},
        )
        assert resp.status_code == 409, resp.get_json()
        assert "用户名已存在" in resp.get_json()["error"]

    def test_register_weak_password(self, client: FlaskClient):
        """Register with a weak password returns 400."""
        # Too short
        resp = client.post(
            "/api/auth/register",
            json={"username": _unique_username(), "password": "short1"},
        )
        assert resp.status_code == 400, resp.get_json()

        # No digit
        resp = client.post(
            "/api/auth/register",
            json={"username": _unique_username(), "password": "onlyletters"},
        )
        assert resp.status_code == 400, resp.get_json()

        # No letter
        resp = client.post(
            "/api/auth/register",
            json={"username": _unique_username(), "password": "12345678"},
        )
        assert resp.status_code == 400, resp.get_json()

    def test_register_missing_fields(self, client: FlaskClient):
        """Register without required fields returns 400."""
        # Empty body
        resp = client.post(
            "/api/auth/register",
            json={},
        )
        assert resp.status_code == 400, resp.get_json()

        # Missing password
        resp = client.post(
            "/api/auth/register",
            json={"username": _unique_username()},
        )
        assert resp.status_code == 400, resp.get_json()

        # Missing username
        resp = client.post(
            "/api/auth/register",
            json={"password": "Pass1234"},
        )
        assert resp.status_code == 400, resp.get_json()


# ---------------------------------------------------------------------------
# Login tests
# ---------------------------------------------------------------------------


class TestLogin:
    """Tests for POST /api/auth/login."""

    @pytest.fixture(autouse=True)
    def _setup_user(self, client: FlaskClient):
        """Register a user before each test in this class."""
        self.username = _unique_username()
        self.password = "LoginPass1"
        resp = client.post(
            "/api/auth/register",
            json={"username": self.username, "password": self.password},
        )
        assert resp.status_code == 201, f"Setup failed: {resp.get_json()}"

    def test_login_success(self, client: FlaskClient):
        """Login with valid credentials returns 200, token, and user info."""
        resp = client.post(
            "/api/auth/login",
            json={"username": self.username, "password": self.password},
        )
        assert resp.status_code == 200, resp.get_json()
        data = resp.get_json()
        assert "token" in data
        assert "user" in data
        assert data["user"]["username"] == self.username
        assert "id" in data["user"]
        # Token should be a non-empty string
        assert len(data["token"]) > 0

    def test_login_wrong_password(self, client: FlaskClient):
        """Login with wrong password returns 401."""
        resp = client.post(
            "/api/auth/login",
            json={"username": self.username, "password": "WrongPass1"},
        )
        assert resp.status_code == 401, resp.get_json()
        assert "用户名或密码错误" in resp.get_json()["error"]

    def test_login_nonexistent_user(self, client: FlaskClient):
        """Login with a non-existent username returns 401."""
        resp = client.post(
            "/api/auth/login",
            json={"username": _unique_username(), "password": "Pass1234"},
        )
        assert resp.status_code == 401, resp.get_json()
        assert "用户名或密码错误" in resp.get_json()["error"]

    def test_login_missing_fields(self, client: FlaskClient):
        """Login with missing fields returns 400."""
        # Empty body
        resp = client.post("/api/auth/login", json={})
        assert resp.status_code == 400, resp.get_json()

        # Missing password
        resp = client.post(
            "/api/auth/login",
            json={"username": self.username},
        )
        assert resp.status_code == 400, resp.get_json()
