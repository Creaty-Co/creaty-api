from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as _UserManager


class UserManager(_UserManager):
    def create_user(self, email, password=None, first_name=None, **extra_fields):
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
