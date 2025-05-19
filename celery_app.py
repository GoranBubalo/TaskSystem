from celery import Celery
import os

# Redis as broker and backend
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Create Celery instance
celery_app = Celery(
    "taskflow",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["Task.app.service.celery_tasks"]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    worker_prefetch_multiplier=1,  # Prevent worker from prefetching too many tasks
)

if __name__ == "__main__":
    celery_app.start()