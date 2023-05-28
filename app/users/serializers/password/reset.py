from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from app.base.exceptions import APIWarning
from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class POSTUsersPasswordResetSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['email']

    def validate(self, attrs):
        get_object_or_404(User, **attrs)
        return attrs


class PUTUsersPasswordResetSerializer(BaseModelSerializer):
    WARNINGS = {
        408: APIWarning(
            "Password reset code has been expired",
            408,
            'password_reset_code_timed_out',
        )
    }

    code = serializers.IntegerField()

    class Meta:
        model = User
        extra_kwargs = {'new_password': {'source': 'password'}}
        write_only_fields = ['email', 'code', 'new_password']

    def validate(self, attrs):
        validate_password(attrs['password'], User(email=attrs['email']))
        return attrs
