FROM python:3.10

WORKDIR /api

COPY /requirements.txt /api/requirements.txt
RUN pip install --upgrade pip \ pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=api.settings

COPY . /api

RUN python manage.py collectstatic --no-input
