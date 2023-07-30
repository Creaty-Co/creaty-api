import time

from django.core.exceptions import ValidationError
from django.db import models

from app.base.models.base import BaseModel


def category_icon_upload_to(instance, _):
    return f"category/icon/{instance.id}-{int(time.time())}"


class Category(BaseModel):
    shortcut = models.TextField(unique=True)
    title = models.TextField()
    icon = models.ImageField(upload_to=category_icon_upload_to)

    def clean(self):
        super().clean()
        if Tag.objects.filter(shortcut=self.shortcut).exists():
            raise ValidationError(f"Tag with shortcut {self.shortcut} already exists")

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.icon.name.split('/')[-1].rsplit('-', 1)[0] != str(self.id):
            self.icon.save(None, self.icon.file)

    def __str__(self):
        return f"Category: {self.title} ({self.shortcut})"


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
                f"Category with shortcut {self.shortcut} already exists"
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
