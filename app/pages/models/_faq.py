from django.db import models

from app.base.models.base import BaseModel

__all__ = ['Faq']


class Faq(BaseModel):
    question = models.TextField()
    answer = models.TextField()
