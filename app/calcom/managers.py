from django.db import models


class BaseCalManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('cal')
