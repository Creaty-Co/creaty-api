from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager as _UserManager


class UserManager(_UserManager):
    def _create_user(self, email, password, first_name, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email=None, password=None, first_name=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, first_name, **extra_fields)
    
    def create_superuser(
        self, email=None, password=None, first_name=None, **extra_fields
    ):
        extra_fields['is_superuser'] = True
        return self._create_user(email, password, first_name, **extra_fields)
