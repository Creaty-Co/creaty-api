from django.db import models

from base.models import AbstractModel


class Subscribe(AbstractModel):
    email = models.EmailField()
