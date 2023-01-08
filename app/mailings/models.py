import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from app.base.models.base import BaseModel


class Subscriber(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()


class Mailing(BaseModel):
    subject = models.TextField()
    content = models.TextField()
    is_stopped = models.BooleanField(default=True)
    task_ids = ArrayField(models.TextField(), blank=True, null=True)
