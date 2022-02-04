from rest_framework import serializers

from mailings.models import Subscribe


class MailingsSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['email']
