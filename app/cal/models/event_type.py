from django.db import models

from app.cal.models.base import BaseCalModel


class CalEventType(BaseCalModel):
    slug = models.TextField()

    class Meta:
        db_table = 'EventType'
