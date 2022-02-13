from rest_framework import serializers

from mailings.serializers.base import BaseMailingsSerializer


class MailingSerializer(BaseMailingsSerializer):
    is_running = serializers.SerializerMethodField()
    
    class Meta(BaseMailingsSerializer.Meta):
        fields = ['id', 'subject', 'content', 'is_running']
