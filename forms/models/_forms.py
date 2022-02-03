from django.contrib.postgres.fields import ArrayField
from django.db import models

from base.models import AbstractModel
from forms.models.choices import FormType, FormField

__all__ = ['Form', 'Application']


class Form(AbstractModel):
    type = models.TextField(unique=True, choices=FormType.choices)
    description = models.TextField(null=True, blank=True)
    fields = ArrayField(models.TextField(choices=FormField.choices))


class Application(AbstractModel):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    name = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telegram = models.TextField(null=True, blank=True)
    facebook = models.TextField(null=True, blank=True)
    whats_app = models.TextField(null=True, blank=True)
    viber = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
