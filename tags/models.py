from django.db import models

from base.models import AbstractModel


class Category(AbstractModel):
    title = models.TextField()


class Tag(AbstractModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.TextField()
