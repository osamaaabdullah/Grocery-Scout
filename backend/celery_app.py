from backend.core.config import get_settings
from celery import Celery

settings = get_settings()

celery = Celery("scraper", broker=settings.redis_url, include=["backend.tasks"] )

celery.conf.update(
    task_serializer="json",
    task_ignore_result=True,
    worker_concurrency=5
)
