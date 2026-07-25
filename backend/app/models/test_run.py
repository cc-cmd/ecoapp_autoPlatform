"""TestRun model.

Represents the execution of a single test case within a batch.
Each test_run goes through the state machine:
    queued -> running -> passed / failed / error

Once a terminal state is reached, the transition is irreversible.
Duration is computed from timestamps, not stored as a column.
"""

import uuid

from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.extensions import db
from app.errors import InvalidTransitionError


class TestRun(db.Model):
    """A single execution record for one test case.

    Attributes:
        id: UUID primary key.
        run_group_id: FK to the parent RunGroup.
        case_id: FK to the TestCase being executed.
        status: Current run state (queued / running / passed / failed / error).
        log: Full execution log text.
        started_at: Timestamp when execution began (server UTC).
        finished_at: Timestamp when execution finished (server UTC).
    """

    __tablename__ = "test_runs"

    # ------------------------------------------------------------------
    # Allowed state transitions
    # ------------------------------------------------------------------

    _ALLOWED_TRANSITIONS: dict[str, set[str]] = {
        "queued": {"running"},
        "running": {"passed", "failed", "error"},
        "passed": set(),
        "failed": set(),
        "error": set(),
    }

    TERMINAL_STATUSES = {"passed", "failed", "error"}

    # ------------------------------------------------------------------
    # Columns
    # ------------------------------------------------------------------

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    run_group_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("run_groups.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    case_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("test_cases.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status = db.Column(
        ENUM("queued", "running", "passed", "failed", "error",
             name="run_status_enum"),
        nullable=False,
        default="queued",
        index=True,
    )
    log = db.Column(db.Text, default="")
    started_at = db.Column(db.DateTime, nullable=True, index=True)
    finished_at = db.Column(db.DateTime, nullable=True)

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    run_group = db.relationship(
        "RunGroup", back_populates="runs"
    )
    test_case = db.relationship(
        "TestCase", back_populates="runs"
    )

    # ------------------------------------------------------------------
    # State machine
    # ------------------------------------------------------------------

    def transition_to(self, new_status: str) -> None:
        """Transition the run to *new_status* if allowed.

        Args:
            new_status: Target status string.

        Raises:
            InvalidTransitionError: If the transition is not allowed
                or the current state is terminal.
        """
        allowed = self._ALLOWED_TRANSITIONS.get(self.status, set())
        if new_status not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from '{self.status}' to '{new_status}'"
            )
        self.status = new_status

    def append_log(self, line: str) -> None:
        """Append a line to the execution log.

        Args:
            line: Log line to append (a newline is added automatically).
        """
        if self.log is None:
            self.log = ""
        self.log += line + "\n"

    # ------------------------------------------------------------------
    # Derived properties
    # ------------------------------------------------------------------

    @property
    def is_terminal(self) -> bool:
        """True if this run has reached an irreversible final state."""
        return self.status in self.TERMINAL_STATUSES

    @property
    def duration_ms(self) -> int | None:
        """Execution duration in ms, computed from started_at / finished_at.

        Returns None when either timestamp is missing.
        """
        if self.started_at and self.finished_at:
            return int(
                (self.finished_at - self.started_at).total_seconds() * 1000
            )
        return None

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation."""
        return {
            "id": str(self.id),
            "run_group_id": str(self.run_group_id),
            "case_id": str(self.case_id),
            "test_case_name": self.test_case.name if self.test_case else None,
            "status": self.status,
            "log": self.log,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration_ms": self.duration_ms,
        }

    def __repr__(self) -> str:
        return f"<TestRun {self.id} [{self.status}]>"
