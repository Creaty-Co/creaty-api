import os

bind = '0.0.0.0:8000'
workers = int(os.getenv('GUNICORN_WORKERS'))
max_requests = 100
