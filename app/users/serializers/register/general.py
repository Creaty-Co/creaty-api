from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from app.base.exceptions import APIWarning
from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class _EmailUniqueValidator(UniqueValidator):
    def __call__(self, value, serializer_field):
        try:
            super().__call__(value, serializer_field)
        except ValidationError:
            raise POSTUsersRegisterSerializer.WARNINGS[409]


class POSTUsersRegisterSerializer(BaseModelSerializer):
    WARNINGS = {
        409: APIWarning(
            "User with this email already exists",
            409,
            'register_email_already_exists',
        )
    }

    class Meta:
        model = User
        extra_kwargs = {
            'email': {'validators': [_EmailUniqueValidator(User.objects.all())]}
        }
        write_only_fields = ['first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        validate_password(attrs['password'], User(**attrs))
        return attrs
