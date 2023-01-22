from drf_base64.fields import Base64FileField

from app.base.serializers.base import BaseModelSerializer
from app.pages.models import SocialLink


class ListPagesLinksSocialsSerializer(BaseModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'icon', 'url']


class CreatePagesLinksSocialsSerializer(BaseModelSerializer):
    icon = Base64FileField(write_only=True)

    class Meta:
        model = SocialLink
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'icon': {}, 'url': wo}
        fields = list(extra_kwargs.keys())


class PagesLinksSocialSerializer(BaseModelSerializer):
    icon = Base64FileField(write_only=True)

    class Meta:
        model = SocialLink
        wo = {'write_only': True}
        extra_kwargs = {'icon': {}, 'url': wo}
        fields = list(extra_kwargs.keys())
