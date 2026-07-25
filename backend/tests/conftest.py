"""Pytest fixtures for the automation platform backend.

Provides a fully configured Flask test app, client, database session,
and authentication helpers.  Uses the development config which connects
to the real PostgreSQL database (tables must already exist).
"""

import uuid

import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import select

from app import create_app
from app.extensions import db as _db
from app.models.user import User


@pytest.fixture(scope="session")
def app() -> Flask:
    """Create the Flask application with the development config.

    The database must already exist with all tables created (Alembic).
    Tables are NOT dropped or recreated between test sessions.
    """
    _app = create_app("development")
    _app.config.update({"TESTING": True})
    return _app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def db_session(app: Flask):
    """Provide a database session for tests.

    Each test runs inside a transaction that is rolled back at
    the end, ensuring test isolation.
    """
    with app.app_context():
        conn = _db.engine.connect()
        tx = conn.begin()
        try:
            yield _db.session
        finally:
            tx.rollback()
            conn.close()


@pytest.fixture
def auth_token(client: FlaskClient) -> str:
    """Register a unique test user and return a JWT access token.

    Uses a random suffix to avoid conflicts with existing data.
    The test user is cleaned up after the test.
    """
    suffix = uuid.uuid4().hex[:8]
    username = f"testuser_{suffix}"
    password = "testpass123"

    # Register
    resp = client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 201, f"Register failed: {resp.get_json()}"

    # Login
    resp = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 200, f"Login failed: {resp.get_json()}"

    token = resp.get_json()["token"]

    # Clean up after test
    yield token

    with client.application.app_context():
        user = _db.session.scalar(
            select(User).where(User.username == username)
        )
        if user:
            _db.session.delete(user)
            _db.session.commit()
