FROM python:3.12.6

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=api.settings

COPY /requirements.txt ./requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip  \
    pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt

COPY . .
