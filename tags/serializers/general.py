from rest_framework import serializers

from tags.models import Tag


class ListTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'shortcut', 'title']
