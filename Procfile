web: gunicorn --workers=3 api.wsgi
worker: cd merlines/ && celery -A api worker -c 3 -P gevent
