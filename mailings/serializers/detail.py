from rest_framework import serializers

from mailings.models import Mailing


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ['id', 'subject', 'content']
