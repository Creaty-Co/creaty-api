from celery import shared_task

# noinspection PyUnresolvedReferences
from sentry_sdk.crons.decorator import monitor


@shared_task
@monitor(monitor_slug='check_health')
def check_health():
    pass
