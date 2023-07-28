from django.db import models

from app.base.models.base import BaseModel

__all__ = ['Faq']


class Faq(BaseModel):
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question if len(self.question) < 50 else self.question[:50] + '...'
