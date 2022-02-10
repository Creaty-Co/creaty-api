from django.db import models

from base.models import AbstractModel

__all__ = ['Faq']


class Faq(AbstractModel):
    question = models.TextField()
    answer = models.TextField()
