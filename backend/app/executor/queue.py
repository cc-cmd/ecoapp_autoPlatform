"""Simple in-memory execution queue.

Provides thread-safe enqueue / dequeue operations for notifying the
executor about newly-triggered batches. The queue holds batch IDs.

Real-world use would likely involve a database-backed queue (polling
the run_groups table), but an in-memory side-queue reduces latency
when the scheduler polls the DB every N seconds.
"""

import threading
from collections import deque


class ExecutionQueue:
    """Thread-safe FIFO queue for batch execution notifications.

    Operations:
      - enqueue(batch_id): Add a batch ID to the queue.
      - dequeue():         Pop the next batch ID (non-blocking).
      - pending_count:     Number of items currently in the queue.
    """

    def __init__(self):
        self._queue: deque[str] = deque()
        self._lock = threading.Lock()

    def enqueue(self, batch_id: str) -> None:
        """Add a batch ID to the queue.

        Args:
            batch_id: UUID of the RunGroup to execute.
        """
        # TODO: Implement enqueue
        #   - with self._lock: self._queue.append(batch_id)
        pass

    def dequeue(self) -> str | None:
        """Pop the next batch ID from the queue (non-blocking).

        Returns:
            Batch UUID string, or None if the queue is empty.
        """
        # TODO: Implement dequeue
        #   - with self._lock: return self._queue.popleft() if queue else None
        ...
        return None

    @property
    def pending_count(self) -> int:
        """Number of items waiting in the queue."""
        # TODO: Implement pending_count
        #   - with self._lock: return len(self._queue)
        return 0
