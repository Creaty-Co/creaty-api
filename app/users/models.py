from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.db import models

from app.base.models.base import BaseModel
from app.users.managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.TextField()
    last_name = models.TextField(default='', blank=True)
    is_staff = models.BooleanField(default=False)
    has_discount = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    is_active = True

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = EMAIL_FIELD
    REQUIRED_FIELDS = []

    @property
    def is_mentor(self) -> bool:
        from app.mentors.models import Mentor

        return Mentor.objects.filter(email=self.email).exists()

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def set_password(self, raw_password):
        validate_password(raw_password, self)
        super().set_password(raw_password)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
