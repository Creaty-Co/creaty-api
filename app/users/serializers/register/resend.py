from app.base.exceptions import APIWarning
from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


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
        write_only_fields = ['email']
