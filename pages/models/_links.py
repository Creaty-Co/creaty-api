from django.db import models

from base.models import AbstractModel
from pages.models.choices import DocumentLinkType

__all__ = ['SocialLink', 'DocumentLink']


class SocialLink(AbstractModel):
    icon = models.ImageField(upload_to='pages/social_link/icon')
    url = models.TextField()


class DocumentLink(AbstractModel):
    type = models.TextField(choices=DocumentLinkType.choices, unique=True)
    url = models.TextField()
