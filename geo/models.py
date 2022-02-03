from django.db import models

from base.models import AbstractModel

__all__ = ['Country', 'Language']


class Country(AbstractModel):
    code = models.CharField(max_length=2, unique=True)
    flag_unicode = models.CharField(max_length=11, unique=True)
    name = models.TextField()


class Language(AbstractModel):
    code = models.CharField(max_length=7, unique=True)
    name = models.TextField()
    name_native = models.TextField()
