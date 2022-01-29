import os

from celery import Celery
from celery.signals import after_task_publish

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')

app = Celery('api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@after_task_publish.connect
def update_sent_state(sender=None, headers=None, **_):
    task = app.tasks.get(sender)
    backend = task.backend if task else app.backend
    backend.store_result(headers['id'], None, 'SENT')
