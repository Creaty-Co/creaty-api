web: gunicorn --workers=4 api.wsgi
celery_worker: (celery -A api worker -c 2 -P gevent -l info &) && (celery -A api beat -S django -l info)
