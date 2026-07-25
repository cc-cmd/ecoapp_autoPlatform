"""Report and statistics service.

Provides aggregated data for the dashboard summary and per-batch reports.
"""

from sqlalchemy.orm import Session as DBSession


class ReportService:
    """Reporting business logic."""

    def __init__(self, db_session: DBSession):
        self.db = db_session

    def get_summary(self, days: int = 7) -> dict:
        """Get aggregated dashboard statistics.

        Args:
            days: Lookback window in days for recent statistics.

        Returns:
            Dictionary with keys:
              - total_cases: Total number of test cases.
              - total_runs: Total number of executed runs.
              - pass_rate: Overall pass rate (0.0 - 1.0).
              - automated_count: Number of automated test cases.
              - recent_batches: Last 10 run batches.
              - daily_stats: Per-day aggregated stats for the lookback period.
        """
        # TODO: Implement get_summary
        #   - Count total test cases
        #   - Count automated test cases
        #   - Count total completed runs in lookback period
        #   - Calculate pass rate (passed / total)
        #   - Query last 10 batches with basic info
        #   - Aggregate daily stats (date -> {passed, failed, error, total})
        #   - Return combined dict
        raise NotImplementedError

    def get_detail(self, batch_id: str) -> dict:
        """Get detailed report for a specific batch.

        Args:
            batch_id: RunGroup UUID.

        Returns:
            Dictionary with keys:
              - batch: Batch metadata dict.
              - runs: List of test run dicts.
              - summary: {
                    total, passed, failed, error,
                    pass_rate, total_duration_ms
                }

        Raises:
            NotFoundError: If the batch does not exist.
        """
        # TODO: Implement get_detail
        #   - Get RunGroup with all TestRuns
        #   - Raise NotFoundError if missing
        #   - Calculate summary stats
        #   - Return combined dict
        raise NotImplementedError
