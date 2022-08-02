web: gunicorn --workers=12 api.wsgi
celery_worker: (celery -A api worker -c 3 -P gevent -l info &) && (celery -A api beat -S django -l info)
