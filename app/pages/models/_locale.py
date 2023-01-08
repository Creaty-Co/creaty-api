from django.conf import settings
from django.db import models

from app.base.models.base import BaseModel


class Locale(BaseModel):
    language = models.TextField(unique=True, choices=settings.LANGUAGES)
    json = models.JSONField()
