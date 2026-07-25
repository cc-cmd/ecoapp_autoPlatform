"""Run execution service.

Handles triggering new execution batches, querying batch/run state,
and cancelling queued or in-progress runs.
"""

from sqlalchemy.orm import Session as DBSession

from app.models.run_group import RunGroup
from app.models.test_run import TestRun
from app.errors import NotFoundError, ValidationError, InvalidTransitionError


class RunService:
    """Run execution business logic."""

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def trigger(
        self,
        case_ids: list[str],
        triggered_by: str,
        name: str | None = None,
        device_id: str | None = None,
    ) -> tuple[RunGroup, list[TestRun]]:
        """Trigger a new execution batch.

        Creates a RunGroup and individual TestRun records for each
        case. If no device_id is provided, the system will attempt to
        auto-allocate one via the device allocator.

        Args:
            case_ids: List of test case UUIDs to execute.
            triggered_by: UUID of the user who triggered the batch.
            name: Optional batch name (auto-generated if omitted).
            device_id: Optional device UUID (auto-allocate if omitted).

        Returns:
            Tuple of (RunGroup, list of TestRun instances).

        Raises:
            ValidationError: If case_ids is empty or contains invalid IDs.
            DeviceNotAvailableError: If no device is available.
        """
        # TODO: Implement trigger
        #   - Validate case_ids (non-empty, all exist)
        #   - If device_id provided, verify device exists and is online
        #   - If no device_id, call device_service.allocate_device()
        #   - Create RunGroup with status='queued'
        #   - Create TestRun for each case_id with status='queued'
        #   - db.flush()
        #   - Return (run_group, test_runs)
        raise NotImplementedError

    def list_batches(
        self,
        page: int = 1,
        size: int = 20,
        status: str | None = None,
    ) -> tuple[list[RunGroup], int]:
        """List run batches with pagination.

        Args:
            page: Page number (1-based).
            size: Items per page.
            status: Optional filter by batch status.

        Returns:
            Tuple of (list of RunGroup, total count).
        """
        # TODO: Implement list_batches
        #   - Build query with optional status filter
        #   - Order by created_at desc
        #   - Apply pagination
        #   - Return (items, total)
        raise NotImplementedError

    def get_batch_detail(self, batch_id: str) -> tuple[RunGroup, list[TestRun]]:
        """Get a batch and all its child test runs.

        Args:
            batch_id: RunGroup UUID.

        Returns:
            Tuple of (RunGroup, list of TestRun).

        Raises:
            NotFoundError: If the batch does not exist.
        """
        # TODO: Implement get_batch_detail
        #   - Get RunGroup by id (raise NotFound if missing)
        #   - Query TestRuns for this batch, ordered by sort_order
        #   - Return (run_group, test_runs)
        raise NotImplementedError

    def get_run_detail(self, run_id: str) -> TestRun:
        """Get a single test run by ID.

        Args:
            run_id: TestRun UUID.

        Returns:
            TestRun instance.

        Raises:
            NotFoundError: If the run does not exist.
        """
        # TODO: Implement get_run_detail
        #   - db.get(TestRun, run_id)
        #   - Raise NotFoundError if None
        raise NotImplementedError

    def cancel_batch(self, batch_id: str) -> None:
        """Cancel an entire batch.

        Only batches in 'queued' or 'running' state can be cancelled.
        Queued runs are set to 'error'. Running runs are marked 'error'
        and the executor is notified to stop.

        Args:
            batch_id: RunGroup UUID.

        Raises:
            NotFoundError: If the batch does not exist.
            InvalidTransitionError: If batch is already in a terminal state.
        """
        # TODO: Implement cancel_batch
        #   - Get RunGroup (raise NotFound if missing)
        #   - Validate batch.status in ('queued', 'running')
        #   - If running: notify executor to stop
        #   - Set all queued/running child runs to 'error'
        #   - Set batch status to 'completed'
        #   - Update finished_at timestamp
        #   - Release device
        #   - db.flush()
        raise NotImplementedError

    def cancel_run(self, batch_id: str, run_id: str) -> None:
        """Cancel a single run within a batch.

        Only runs in 'queued' or 'running' state can be cancelled.

        Args:
            batch_id: Parent RunGroup UUID.
            run_id: TestRun UUID.

        Raises:
            NotFoundError: If the batch or run does not exist.
            InvalidTransitionError: If the run is already terminal.
        """
        # TODO: Implement cancel_run
        #   - Verify batch exists
        #   - Get TestRun (raise NotFound if missing)
        #   - Verify run.status in ('queued', 'running')
        #   - Set status to 'error', set error_message
        #   - Set finished_at to now
        #   - db.flush()
        raise NotImplementedError
