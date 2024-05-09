from django.db import models


class BasePlatformManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('platform')
