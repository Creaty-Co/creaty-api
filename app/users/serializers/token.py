from rest_framework import serializers

from app.base.exceptions import APIWarning
from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class POST_UsersTokenSerializer(BaseModelSerializer):
    WARNINGS = {401: APIWarning("Invalid credentials", 401, 'invalid_credentials')}

    token = serializers.CharField()

    class Meta:
        model = User
        write_only_fields = ['email', 'password']
        read_only_fields = ['token']
