from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.users.models import User


class GETUsersMeSerializer(BaseModelSerializer):
    is_mentor = serializers.SerializerMethodField()

    class Meta:
        model = User
        read_only_fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'has_discount',
            'is_verified',
            'is_staff',
            'is_mentor',
        ]

    def get_is_mentor(self, user) -> OpenApiTypes.BOOL:
        return user.to_mentor is not None


class PATCHUsersMeSerializer(BaseModelSerializer):
    class Meta:
        model = User
        write_only_fields = ['first_name', 'last_name']
