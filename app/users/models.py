import time
from typing import TYPE_CHECKING

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from app.base.models.base import BaseModel
from app.users.managers import UserManager

if TYPE_CHECKING:
    from app.mentors.models import Mentor


def user_avatar_upload_to(instance, _):
    return f"user/avatar/{instance.id}-{int(time.time())}"


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    social_auth: models.Manager
    email = models.EmailField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField(default='', blank=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_to, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    has_discount = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    is_active = True

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    @property
    def to_mentor(self) -> 'Mentor':
        from app.mentors.models import Mentor

        return Mentor.objects.filter(id=self.id).first()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, **kwargs):
        super().save(**kwargs)
        if self.avatar and self.avatar.name.split('/')[-1].rsplit('-', 1)[0] != str(
            self.id
        ):
            self.avatar.save(None, self.avatar.file)
