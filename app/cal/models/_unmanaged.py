from django.db import models

from app.base.models.base import BaseModel
from app.calcom.managers import BaseCalManager


class CalUser(BaseModel):
    id = models.IntegerField(primary_key=True)
    username = models.TextField()
    email = models.EmailField()

    objects = BaseCalManager()

    class Meta:
        managed = False
        db_table = 'users'
