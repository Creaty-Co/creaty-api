from django.conf import settings
from django.db import models

from base.models import AbstractModel


class Locale(AbstractModel):
    language = models.TextField(unique=True, choices=settings.LANGUAGES)
    json = models.JSONField()
