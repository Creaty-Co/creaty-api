from django.db import models

from app.base.models.base import BaseModel
from app.cal.managers import CalManager


class CalEventType(BaseModel):
    slug = models.TextField()

    objects = CalManager()

    class Meta:
        managed = False
        db_table = 'EventType'
