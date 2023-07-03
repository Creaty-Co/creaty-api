import warnings

import requests
from celery import shared_task
from django.conf import settings
from django.db import connection
from django_redis import get_redis_connection

# noinspection PyUnresolvedReferences
from sentry_sdk.crons.decorator import monitor


@shared_task
@monitor(monitor_slug='check_health')
def check_health():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        assert (
            requests.get(
                f"https://{settings.API_DOMAIN}/base/status/", verify=False
            ).json()['status']
            == "ok"
        )
        assert (
            requests.get(f"https://{settings.WEB_DOMAIN}", verify=False).status_code
            == 200
        )
    assert get_redis_connection().ping()
    connection.ensure_connection()
