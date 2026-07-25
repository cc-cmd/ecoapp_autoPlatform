"""Device allocation with row-level locking.

Uses PostgreSQL ``SELECT ... FOR UPDATE SKIP LOCKED`` to safely
allocate a device under concurrent access. The allocator works with
the database session passed in at construction.
"""

from typing import Set, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from app.models.device import Device, DeviceStatusEnum
from app.errors import DeviceNotAvailableError


class DeviceAllocator:
    """Manages device allocation and release with pessimistic locking.

    Usage::

        allocator = DeviceAllocator(db.session)
        device = allocator.allocate(platform="android")
        # ... run tests ...
        allocator.release(device.id)
    """

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def allocate(
        self,
        platform: str | None = None,
        exclude_ids: Set[str] | None = None,
    ) -> Device:
        """Allocate an available device.

        Selects an online device matching the optional platform filter,
        locks the row with ``FOR UPDATE SKIP LOCKED``, and sets its
        status to 'busy'.

        Args:
            platform: Optional platform filter ("android" / "ios").
            exclude_ids: Optional set of device UUIDs to exclude.

        Returns:
            Allocated Device instance.

        Raises:
            DeviceNotAvailableError: If no matching device is online.
        """
        # TODO: Implement allocate
        #   - Build select(Device).where(Device.status == 'online')
        #   - Apply platform filter if provided
        #   - Apply exclude_ids if provided
        #   - Order by last_heartbeat desc
        #   - .with_for_update(skip_locked=True)
        #   - .first()
        #   - If None: raise DeviceNotAvailableError
        #   - Set device.status = 'busy'
        #   - db.flush()
        #   - Return device
        raise NotImplementedError

    def release(self, device_id: str) -> None:
        """Release a device back to 'online' status.

        Args:
            device_id: UUID of the device to release.

        Raises:
            NotFoundError: If the device does not exist.
        """
        # TODO: Implement release
        #   - db.get(Device, device_id)
        #   - Raise NotFoundError if None
        #   - Set device.status = 'online'
        #   - Update last_heartbeat
        #   - db.flush()
        raise NotImplementedError
