"""Device model.

Represents a physical or virtual test device discovered via ADB / iOS
tools.  Status is maintained by heartbeat; devices that miss their
heartbeat window (> 60 s) are marked offline.
"""

import uuid

from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.extensions import db


class Device(db.Model):
    """A test device (real or emulated).

    Attributes:
        id: UUID primary key (internal).
        device_id: ADB serial or iOS UDID, unique.
        platform: Mobile platform (android / ios).
        model: Device model name.
        status: Current connectivity status (online / busy / offline).
        last_heartbeat: Timestamp of the last heartbeat (server UTC).
    """

    __tablename__ = "devices"

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    device_id = db.Column(
        db.String(128), unique=True, nullable=False, index=True
    )
    platform = db.Column(
        ENUM("android", "ios", name="platform_enum"),
        nullable=False,
    )
    model = db.Column(db.String(128), nullable=False)
    status = db.Column(
        ENUM("online", "busy", "offline", name="device_status_enum"),
        nullable=False,
        default="online",
        index=True,
    )
    last_heartbeat = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False,
        index=True,
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    run_groups = db.relationship(
        "RunGroup", back_populates="device", lazy="dynamic"
    )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        """Return a JSON-serialisable representation."""
        return {
            "id": str(self.id),
            "device_id": self.device_id,
            "platform": self.platform,
            "model": self.model,
            "status": self.status,
            "last_heartbeat": (
                self.last_heartbeat.isoformat() if self.last_heartbeat else None
            ),
        }

    def __repr__(self) -> str:
        return f"<Device {self.device_id} [{self.status}]>"
