from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models

from account.managers.user import UserManager
from account.models.choices import UserType
from base.models import AbstractModel

__all__ = ['User']


class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    type = models.PositiveSmallIntegerField(
        choices=UserType.choices, default=UserType.ADMIN
    )
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
