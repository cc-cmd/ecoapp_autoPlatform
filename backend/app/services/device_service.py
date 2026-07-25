"""Device management service.

Handles device discovery, heartbeat monitoring, and allocation for
test execution.
"""

from datetime import datetime, timezone
from sqlalchemy.orm import Session as DBSession

from app.models.device import Device
from app.errors import DeviceNotAvailableError


class DeviceService:
    """Device business logic."""

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def list_devices(
        self,
        platform: str | None = None,
        status: str | None = None,
    ) -> list[Device]:
        """List devices with optional filtering.

        Args:
            platform: Optional filter by platform ("android" / "ios").
            status: Optional filter by status ("online" / "busy" / "offline").

        Returns:
            List of Device instances matching the filters.
        """
        # TODO: Implement list_devices
        #   - Build query with optional filters
        #   - Order by last_heartbeat desc
        #   - Return device list
        raise NotImplementedError

    def discover(self) -> list[Device]:
        """Discover devices via ADB and iOS device tools.

        New devices are created, existing devices are updated with fresh
        metadata and their heartbeat is refreshed.

        Returns:
            List of Device instances that were created or updated.
        """
        # TODO: Implement discover
        #   - Call adb_utils.list_android_devices()
        #   - Call adb_utils.list_ios_devices()
        #   - For each discovered device:
        #     - Query by udid
        #     - If exists: update fields + heartbeat
        #     - If new: create Device record
        #   - db.flush()
        #   - Return all updated/created devices
        raise NotImplementedError

    def update_heartbeat(self, device_id: str) -> Device:
        """Update a device's last_heartbeat to now.

        Args:
            device_id: Device UUID.

        Returns:
            Updated Device instance.

        Raises:
            NotFoundError: If device not found.
        """
        # TODO: Implement update_heartbeat
        #   - Get device by id
        #   - Set last_heartbeat = datetime.now(timezone.utc)
        #   - If status was offline, set to online
        #   - Return device
        raise NotImplementedError

    def check_offline_devices(self, timeout_seconds: int = 60) -> int:
        """Mark devices as offline if heartbeat is older than timeout.

        Args:
            timeout_seconds: Seconds after which a device is considered offline.

        Returns:
            Number of devices marked offline.
        """
        # TODO: Implement check_offline_devices
        #   - Query devices where status in ('online', 'busy')
        #     AND last_heartbeat < NOW() - timeout
        #   - Set status to 'offline'
        #   - Return count
        raise NotImplementedError

    def allocate_device(
        self,
        platform: str | None = None,
        exclude_ids: set[str] | None = None,
    ) -> Device | None:
        """Allocate an available (online) device, optionally by platform.

        Uses SELECT ... FOR UPDATE SKIP LOCKED to safely pick an idle
        device under concurrency.

        Args:
            platform: Optional platform filter.
            exclude_ids: Set of device IDs to exclude.

        Returns:
            Allocated Device with status set to 'busy', or None if none
            available.
        """
        # TODO: Implement allocate_device
        #   - Build query: status == 'online'
        #   - Apply platform filter, exclude_ids
        #   - Order by last_heartbeat desc
        #   - Apply .with_for_update(skip_locked=True)
        #   - .first()
        #   - If found: set status to 'busy', flush, return
        #   - Return None
        raise NotImplementedError

    def release_device(self, device_id: str) -> None:
        """Release a device back to online status.

        Args:
            device_id: Device UUID.

        Raises:
            NotFoundError: If device not found.
        """
        # TODO: Implement release_device
        #   - Get device
        #   - Set status to 'online'
        #   - Update last_heartbeat
        #   - flush
        raise NotImplementedError
