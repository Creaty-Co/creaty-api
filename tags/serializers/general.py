from rest_framework import serializers

from tags.models import Tag


class ListTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'shortcut', 'title']


class CreateTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'shortcut': wo, 'title_ru': wo, 'title_en': wo}
        fields = list(extra_kwargs.keys())
