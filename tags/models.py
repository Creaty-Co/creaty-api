from django.db import models

from base.models import AbstractModel

__all__ = ['Category', 'Tag']


class Category(AbstractModel):
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    icon = models.ImageField(upload_to='tags/category/icon')


class Tag(AbstractModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    shortcut = models.TextField(unique=True)
    title = models.TextField()
