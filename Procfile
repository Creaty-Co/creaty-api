web: gunicorn --workers=3 api.wsgi
worker: celery -A api worker -c 3 -P gevent -l info
worker: celery -A api beat -S django -l info