from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from app.base.exceptions import APIWarning
from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class POSTUsersPasswordResetSerializer(BaseModelSerializer):
    WARNINGS = {
        404: APIWarning(
            "User with such an email hasn't registered",
            404,
            'password_reset_email_not_found',
        ),
    }

    class Meta:
        model = User
        write_only_fields = ['email']

    def validate(self, attrs):
        if not User.objects.filter(email=attrs['email']).exists():
            raise self.WARNINGS[404]
        return attrs


class PUTUsersPasswordResetSerializer(BaseModelSerializer):
    WARNINGS = {
        408: APIWarning(
            "Password reset code has been expired",
            408,
            'password_reset_code_timed_out',
        )
    }

    code = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()

    class Meta:
        model = User
        extra_kwargs = {'new_password': {'source': 'password'}}
        write_only_fields = ['code', 'new_password']
        read_only_fields = ['access', 'refresh']

    def to_representation(self, instance):
        token: RefreshToken = RefreshToken.for_user(instance)
        instance.access = str(token.access_token)
        instance.refresh = str(token)
        return super().to_representation(instance)
