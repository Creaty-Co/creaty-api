from django.db import models

from app.base.models.base import BaseModel
from app.pages.models.choices import DocumentLinkType

__all__ = ['SocialLink', 'DocumentLink']


class SocialLink(BaseModel):
    icon = models.ImageField(upload_to='pages/social_link/icon')
    url = models.TextField()


class DocumentLink(BaseModel):
    type = models.TextField(choices=DocumentLinkType.choices, unique=True)
    url = models.TextField()
