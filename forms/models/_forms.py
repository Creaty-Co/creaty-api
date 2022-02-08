from django.db import models

from base.models import AbstractModel
from forms.models.choices import FormField, FormType

__all__ = ['Form', 'Field', 'Application']


class Form(AbstractModel):
    type = models.TextField(unique=True, choices=FormType.choices)
    description = models.TextField(blank=True)
    post_send = models.TextField()


class Field(AbstractModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    type = models.TextField(choices=FormField.choices)
    placeholder = models.TextField()
    
    class Meta:
        unique_together = ('form', 'type')


class Application(AbstractModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telegram = models.TextField(blank=True)
    facebook = models.TextField(blank=True)
    whats_app = models.TextField(blank=True)
    viber = models.TextField(blank=True)
    about = models.TextField(blank=True)
