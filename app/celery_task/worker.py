from celery import Celery

from common.config import *
from celery.exceptions import SoftTimeLimitExceeded

CELERY_BROKER_URL = REDIS_INSTANCE
CELERY_RESULT_BACKEND = REDIS_INSTANCE

celery_worker = Celery(
    "celery",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND)


celery_worker.conf.update(
    redis_max_connections = 10000,
    broker_pool_limit = 5000,
)
