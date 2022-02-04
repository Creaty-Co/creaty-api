from rest_framework import serializers

from mailings.models import Subscriber


class MailingsSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email']
