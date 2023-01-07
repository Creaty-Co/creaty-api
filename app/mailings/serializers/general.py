from rest_framework import serializers

from app.base.serializers.base import BaseModelSerializer
from app.mailings.models import Mailing
from app.mailings.serializers.base import BaseMailingsSerializer


class MailingsListSerializer(BaseMailingsSerializer):
    is_running = serializers.SerializerMethodField()

    class Meta(BaseMailingsSerializer.Meta):
        fields = ['id', 'subject', 'is_running']


class MailingsCreateSerializer(BaseModelSerializer):
    class Meta:
        model = Mailing
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'subject': wo, 'content': wo}
        fields = list(extra_kwargs.keys())
