import requests
from celery import shared_task, states


@shared_task(bind=True,
             name='xxx_execute_xx_task',
             max_retries=3,
             soft_time_limit=20)
def xxx_execute_xx_task(self):
    # do something
    data = requests.get(url='https://stackoverflow.com/questions/32449845/'
                            'how-to-run-a-django-celery-task-every-6am-and-6pm-daily')
if data.status_code == 200:
    task.update_state(state=states.SUCCESS)
    if data:
        self.update_state(state=states.SUCCESS)
    else:
        self.update_state(state=states.FAILURE)
