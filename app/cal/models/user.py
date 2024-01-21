from django.db import models

from app.cal.models.base import BaseCalModel


class CalUser(BaseCalModel):
    username = models.TextField()
    name = models.TextField()
    email = models.EmailField()
    role = models.TextField()

    class Meta:
        db_table = 'users'
