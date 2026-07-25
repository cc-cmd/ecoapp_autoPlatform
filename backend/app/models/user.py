"""User model.

Stores authentication credentials and basic profile information.
Passwords are hashed with bcrypt before persistence.
"""

import uuid

import bcrypt
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class User(db.Model):
    """System user.

    Attributes:
        id: UUID primary key (PostgreSQL native).
        username: Unique login name (3-64 chars).
        password_hash: Bcrypt hash of the user's password.
        created_at: Timestamp of account creation (server UTC).
    """

    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username = db.Column(
        db.String(64), unique=True, nullable=False, index=True
    )
    password_hash = db.Column(
        db.String(256), nullable=False
    )
    created_at = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    test_cases = db.relationship(
        "TestCase", back_populates="creator", lazy="dynamic"
    )
    run_groups = db.relationship(
        "RunGroup", back_populates="trigger_user", lazy="dynamic"
    )

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------

    def set_password(self, password: str) -> None:
        """Hash *password* with bcrypt and store it.

        Args:
            password: Plain-text password.
        """
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode(), salt).decode()

    def check_password(self, password: str) -> bool:
        """Verify *password* against the stored hash.

        Args:
            password: Plain-text password to verify.

        Returns:
            True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(
            password.encode(), self.password_hash.encode()
        )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation (never exposes the hash)."""
        return {
            "id": str(self.id),
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self) -> str:
        return f"<User {self.username!r}>"
