from rest_framework import serializers

from account.models import User
from account.models.choices import UserType
from base.utils.functions import choices_to_help_text


class RetrieveAccountsMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {'type': {'help_text': choices_to_help_text(UserType)}}
        fields = ['email', 'first_name', 'last_name', 'type']


class UpdateMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        wo = {'write_only': True}
        extra_kwargs = {'first_name': wo, 'last_name': wo}
        fields = list(extra_kwargs.keys())
