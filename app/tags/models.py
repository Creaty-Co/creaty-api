from django.core.exceptions import ValidationError
from django.db import models

__all__ = ['Category', 'Tag']

from app.base.models.base import BaseModel


class Category(BaseModel):
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    icon = models.ImageField(upload_to='tags/category/icon')

    def clean(self):
        super().clean()
        if Tag.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(f'Тег с shortcut {self.shortcut} уже существует')


class Tag(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    shortcut = models.TextField(unique=True)
    title = models.TextField()

    def clean(self):
        super().clean()
        if Category.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(
                f'Категория с shortcut {self.shortcut} уже существует'
            )
