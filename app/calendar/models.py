from django.db import models

from app.base.models.base import BaseModel
from app.users.models import User


class CalendarEvent(BaseModel):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    title = models.TextField()
    host = models.TextField()
    guests = models.ManyToManyField(User)
    google_event_uuid = models.UUIDField(unique=True)
