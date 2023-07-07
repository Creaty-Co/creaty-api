import requests
from celery import shared_task
from django.db import connection
from django_redis import get_redis_connection

# noinspection PyUnresolvedReferences
from sentry_sdk.crons.decorator import monitor


@shared_task
@monitor(monitor_slug='check_health')
def check_health():
    assert requests.get('http://api:8000/base/status/').status_code == 200
    assert get_redis_connection().ping()
    connection.ensure_connection()
