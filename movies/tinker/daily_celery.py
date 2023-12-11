# REFERENCE: https://stackoverflow.com/questions/32449845/how-to-run-a-django-celery-task-every-6am-and-6pm-daily
import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Moex.settings')

app = Celery('Moex',
             backend='rpc://',
             broker='pyamqp://', )

app.config_from_object('django.conf:settings', namespace='CELERY', )

app.conf.update(result_expires=3600,
                enable_utc=True,
                timezone='Europe/Moscow', )

app.conf.beat_schedule = {
    "every day between 6 AM & 18 PM": {
        "task": "xxx_execute_xx_task",  # <---- Name of task
        "schedule": crontab(hour='6, 18',
                            minute=0,
                            )
    },
    "every minute": {
        "task": "check_if_need_update_prices",
        'schedule': 60.0,
    }
}

app.autodiscover_tasks()
