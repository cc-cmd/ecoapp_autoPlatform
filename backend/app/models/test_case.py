"""TestCase model.

Stores metadata about each test case, including priority, automation
status, associated script path, and category membership.
"""

import uuid

from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.extensions import db


class TestCase(db.Model):
    """A single test case definition.

    Attributes:
        id: UUID primary key.
        name: Test case title.
        priority: Priority level (P0/P1/P2/P3, default P3).
        steps: Human-readable test steps (plain text).
        script_path: Relative path to the uploaded Python script (optional).
        is_automated: Whether an automated script exists.
        category_id: FK to Category.
        created_by: FK to User who created the case.
        created_at: Creation timestamp (server UTC).
        updated_at: Last-update timestamp (auto-refreshed on PUT).
    """

    __tablename__ = "test_cases"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name = db.Column(db.String(255), nullable=False)
    priority = db.Column(
        ENUM("P0", "P1", "P2", "P3", name="priority_enum"),
        nullable=False,
        default="P3",
        index=True,
    )
    steps = db.Column(db.Text, default="")
    script_path = db.Column(db.String(512), nullable=True)
    is_automated = db.Column(db.Boolean, nullable=False, default=False)
    category_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        onupdate=db.func.now(),
        nullable=False,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    creator = db.relationship("User", back_populates="test_cases")
    category = db.relationship("Category", back_populates="test_cases")
    runs = db.relationship(
        "TestRun",
        back_populates="test_case",
        lazy="dynamic",
        order_by="TestRun.started_at.desc()",
    )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation with joined names."""
        return {
            "id": str(self.id),
            "name": self.name,
            "priority": self.priority,
            "steps": self.steps,
            "script_path": self.script_path,
            "is_automated": self.is_automated,
            "category_id": str(self.category_id) if self.category_id else None,
            "category_name": self.category.name if self.category else None,
            "created_by": str(self.created_by),
            "creator_name": self.creator.username if self.creator else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self) -> str:
        return f"<TestCase {self.name!r} [{self.priority}]>"
