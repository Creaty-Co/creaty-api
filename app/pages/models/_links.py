import time

from django.db import models

from app.base.models.base import BaseModel
from app.pages.models.choices import DocumentLinkType


def social_link_icon_upload_to(instance, _):
    return f"social_link/icon/{instance.id}-{int(time.time())}"


class SocialLink(BaseModel):
    icon = models.ImageField(upload_to=social_link_icon_upload_to)
    url = models.TextField()

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.icon.name.split('/')[-1].rsplit('-', 1)[0] != str(self.id):
            self.icon.save(None, self.icon.file)


class DocumentLink(BaseModel):
    type = models.TextField(choices=DocumentLinkType.choices, unique=True)
    url = models.TextField()
