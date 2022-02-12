from rest_framework import serializers

from tags.models import Tag


class UpdateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'shortcut': wo, 'title': wo}
        fields = list(extra_kwargs.keys())
