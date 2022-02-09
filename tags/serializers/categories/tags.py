from rest_framework import serializers

from tags.models import Tag


class TagsCategoryTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'shortcut': wo, 'title_ru': wo, 'title_en': wo}
        fields = list(extra_kwargs.keys())
