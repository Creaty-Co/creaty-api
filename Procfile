web: gunicorn --workers=3 api.wsgi
worker: celery -A api worker -c 3 -P gevent
