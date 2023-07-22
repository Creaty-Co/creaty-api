from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import QuerySet

from app.base.models.base import BaseModel
from app.pages.models import Page


def category_icon_upload_to(instance, _):
    return f"category/icon/{instance.shortcut}"


class Category(BaseModel):
    pages: QuerySet
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    icon = models.ImageField(upload_to=category_icon_upload_to)

    @property
    def page(self) -> Page:
        return self.pages.first()

    def clean(self):
        super().clean()
        if Tag.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(f'Тег с shortcut {self.shortcut} уже существует')

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.icon.name.split('/')[-1] != self.shortcut:
            self.icon.save(None, self.icon.file)

    def __str__(self):
        return f"Category: {self.title} ({self.shortcut})"


class Tag(BaseModel):
    pages: QuerySet
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    categories = models.ManyToManyField(
        Category, through='CategoryTag', related_name='tags'
    )

    @property
    def page(self) -> Page | None:
        return self.pages.first()

    def clean(self):
        super().clean()
        if Category.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(
                f'Категория с shortcut {self.shortcut} уже существует'
            )

    def __str__(self):
        return f"Tag: {self.title} ({self.shortcut})"


class CategoryTag(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'tag')

    def __str__(self):
        return f"{self.category.shortcut} ↔ {self.tag.shortcut}"
