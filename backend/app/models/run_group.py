"""RunGroup model.

Represents a batch of test case executions triggered together.
Each trigger call creates one run_group with status='queued'.
All child test_runs share the same device (device is allocated
per batch).
"""

import uuid

from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.extensions import db


class RunGroup(db.Model):
    """A batch of test case executions.

    Counters (total_cases, passed_cases, failed_cases) are computed
    via properties -- they are NOT stored as columns.

    Attributes:
        id: UUID primary key.
        status: Batch state (queued / running / completed).
        triggered_by: FK to User who triggered the batch.
        device_id: FK to Device assigned to this batch (set by executor).
        created_at: Batch creation timestamp (server UTC).
        finished_at: Timestamp when all runs completed (server UTC).
    """

    __tablename__ = "run_groups"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    device_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("devices.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status = db.Column(
        ENUM("queued", "running", "completed", name="run_group_status_enum"),
        nullable=False,
        default="queued",
        index=True,
    )
    triggered_by = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )
    created_at = db.Column(
        db.DateTime, server_default=db.func.now(), nullable=False
    )
    finished_at = db.Column(db.DateTime, nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    device = db.relationship("Device", back_populates="run_groups")
    trigger_user = db.relationship("User", back_populates="run_groups")
    runs = db.relationship(
        "TestRun",
        back_populates="run_group",
        lazy="dynamic",
        order_by="TestRun.id.asc()",
    )

    # ------------------------------------------------------------------
    # State helpers
    # ------------------------------------------------------------------

    TERMINAL_STATUSES = {"completed"}

    @property
    def is_terminal(self) -> bool:
        """True when all runs have completed (any outcome)."""
        return self.status in self.TERMINAL_STATUSES

    @property
    def total_cases(self) -> int:
        """Total number of test runs in this batch."""
        return self.runs.count()

    @property
    def passed_cases(self) -> int:
        """Number of passed runs in this batch."""
        return self.runs.filter_by(status="passed").count()

    @property
    def failed_cases(self) -> int:
        """Number of failed runs in this batch."""
        return self.runs.filter_by(status="failed").count()

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation."""
        return {
            "id": str(self.id),
            "device_id": str(self.device_id) if self.device_id else None,
            "device_model": self.device.model if self.device else None,
            "status": self.status,
            "triggered_by": str(self.triggered_by) if self.triggered_by else None,
            "trigger_username": (
                self.trigger_user.username if self.trigger_user else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "total": self.total_cases,
            "passed": self.passed_cases,
            "failed": self.failed_cases,
        }

    def __repr__(self) -> str:
        return f"<RunGroup {self.id} [{self.status}]>"
