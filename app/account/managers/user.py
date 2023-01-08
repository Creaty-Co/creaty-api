from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as _UserManager

from app.account.enums.users import UserType


class UserManager(_UserManager):
    def create_user(self, email, password='', **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password='', **extra_fields):
        extra_fields['type'] = UserType.SUPER
        return self.create_user(email, password, **extra_fields)
