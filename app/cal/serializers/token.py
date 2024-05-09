from rest_framework import serializers

from app.base.serializers.base import BaseSerializer


class GET_CalTokenSerializer(BaseSerializer):
    token = serializers.CharField(read_only=True)
