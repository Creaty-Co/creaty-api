from django.db import models

__all__ = ['Country', 'Language']

from app.base.models.base import BaseModel


class Country(BaseModel):
    code = models.CharField(max_length=2, unique=True)
    flag_unicode = models.CharField(max_length=11, unique=True)
    name = models.TextField()

    def __str__(self):
        return self.name


class Language(BaseModel):
    code = models.CharField(max_length=7, unique=True)
    name = models.TextField()
    name_native = models.TextField()

    def __str__(self):
        return self.name
