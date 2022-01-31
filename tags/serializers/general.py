from rest_framework import serializers

from tags.models import Tag


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        extra_kwargs = {'id': {}, 'title': {'read_only': True}}
        fields = list(extra_kwargs.keys())
