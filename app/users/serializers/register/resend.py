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
            raise POSTUsersRegisterResendSerializer.WARNINGS[409]


class POSTUsersRegisterResendSerializer(BaseModelSerializer):
    WARNINGS = {
        404: APIWarning(
            "User with such an email hasn't registered",
            404,
            'register_resend_email_not_found',
        ),
        409: APIWarning(
            "User has already been verified", 409, 'register_resend_already_verified'
        ),
    }

    class Meta:
        model = User
        extra_kwargs = {
            'email': {'validators': [_EmailUniqueValidator(User.objects.all())]}
        }
        write_only_fields = ['email']
