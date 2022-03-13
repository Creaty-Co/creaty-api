import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models import AbstractModel


class Subscriber(AbstractModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()


class Mailing(AbstractModel):
    subject = models.TextField()
    content = models.TextField()
    is_stopped = models.BooleanField(default=True)
    task_ids = ArrayField(models.TextField(), blank=True, null=True)
