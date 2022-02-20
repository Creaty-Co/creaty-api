from rest_framework import serializers

from base.serializers.base import BaseSerializer


class BaseFrontErrorSerializer(BaseSerializer):
    subject = serializers.CharField()
    body = serializers.CharField()
