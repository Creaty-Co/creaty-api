from drf_base64.fields import Base64FileField
from rest_framework import serializers

from pages.models import SocialLink


class ListPagesLinksSocialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'icon', 'url']


class CreatePagesLinksSocialsSerializer(serializers.ModelSerializer):
    icon = Base64FileField(write_only=True)
    
    class Meta:
        model = SocialLink
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'icon': {}, 'url': wo}
        fields = list(extra_kwargs.keys())


class PagesLinksSocialSerializer(serializers.ModelSerializer):
    icon = Base64FileField(write_only=True)
    
    class Meta:
        model = SocialLink
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'icon': {}, 'url': wo}
        fields = list(extra_kwargs.keys())
