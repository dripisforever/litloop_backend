from __future__ import absolute_import

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "litloop_project.settings")

broker_url = "amqp://localhost:5672"
BROKER_URL = os.environ.get('RABBITMQ_URL', 'amqp://guest:guest@localhost:5672/')

redis_url = "redis://localhost:6379/0"
rpc_backend = 'rpc://'

# app = Celery("litloop_project", broker=broker_url, backend=rpc_backend)
# app = Celery("litloop_project", broker=broker_url, backend=redis_url, include=['views.tasks'])
app = Celery("litloop_project")

app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

# app.conf.beat_schedule = app.conf.CELERY_BEAT_SCHEDULE
app.conf.broker_transport_options = {"visibility_timeout": 60 * 60 * 24}  # 1 day
# http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html#redis-caveats


app.conf.worker_prefetch_multiplier = 1
