from django.conf import settings
from django.db import models
from django.utils import timezone

from app.base.models.base import BaseModel
from app.forms.models.choices import FormField, FormType

__all__ = ['Form', 'Field', 'Application']


class Form(BaseModel):
    type = models.TextField(unique=True, choices=FormType.choices)
    description = models.TextField(blank=True)
    post_send = models.TextField()

    def __str__(self):
        return self.type


class Field(BaseModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    type = models.TextField(choices=FormField.choices)
    placeholder = models.TextField()

    class Meta:
        unique_together = ('form', 'type')


class Application(BaseModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    path = models.TextField()
    name = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    about = models.TextField(blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def url(self) -> str:
        return f'https://{settings.WEB_DOMAIN}{self.path}'

    def __str__(self):
        return f"{self.form}: {self.path}"
