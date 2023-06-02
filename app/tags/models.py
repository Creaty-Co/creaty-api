from django.core.exceptions import ValidationError
from django.db import models

from app.base.models.base import BaseModel


class Category(BaseModel):
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    icon = models.ImageField(upload_to='tags/category/icon')

    def clean(self):
        super().clean()
        if Tag.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(f'Тег с shortcut {self.shortcut} уже существует')

    def __str__(self):
        return f"{self.shortcut} — {self.title}"


class Tag(BaseModel):
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    categories = models.ManyToManyField(
        Category, through='CategoryTag', related_name='tags'
    )

    def clean(self):
        super().clean()
        if Category.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(
                f'Категория с shortcut {self.shortcut} уже существует'
            )

    def __str__(self):
        return f"{self.shortcut} — {self.title}"


class CategoryTag(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'tag')

    def __str__(self):
        return f"{self.category.shortcut}<->{self.tag.shortcut}"
