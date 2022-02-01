web: gunicorn --workers=3 api.wsgi
celery_worker: celery -A api worker -c 3 -P gevent -l info
celery_beat: celery -A api beat -S django -l info