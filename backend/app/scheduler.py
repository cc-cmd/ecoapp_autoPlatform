"""APScheduler integration.

Two recurring jobs are registered:
  1. heartbeat_check_job — runs every 30 seconds; marks devices as offline
     when heartbeat has been missing for 60+ seconds.
  2. queue_consume_job  — runs every 3 seconds; picks the next queued batch
     and dispatches it to the executor.
"""

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def init_scheduler(app) -> None:
    """Initialise the background scheduler and register recurring jobs.

    Must be called after the app is fully configured. The scheduler is
    started only once (``scheduler.running`` guards against double-start).
    """

    heartbeat_interval = app.config.get("SCHEDULER_HEARTBEAT_INTERVAL", 30)
    queue_interval = app.config.get("SCHEDULER_QUEUE_INTERVAL", 3)

    # TODO: Implement heartbeat_check_job
    #   - Query all devices with status='online' or 'busy'
    #   - Mark as offline where NOW() - last_heartbeat > 60s
    @scheduler.scheduled_job(
        "interval", seconds=heartbeat_interval, id="heartbeat_check"
    )
    def heartbeat_check_job():
        """Check for stale device heartbeats and mark them offline."""
        pass

    # TODO: Implement queue_consume_job
    #   - Fetch the earliest queued run_group
    #   - If found and device is available, transition to running,
    #     spawn executor work
    @scheduler.scheduled_job(
        "interval", seconds=queue_interval, id="queue_consume"
    )
    def queue_consume_job():
        """Pick the next queued batch and dispatch it for execution."""
        pass

    if not scheduler.running:
        scheduler.start()
