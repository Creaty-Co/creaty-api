from rest_framework import serializers

from app.base.serializers.base import BaseSerializer


class GET_CalcomTokenSerializer(BaseSerializer):
    token = serializers.CharField(read_only=True)
