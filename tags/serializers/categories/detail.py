from rest_framework import serializers

from tags.models import Category


class TagsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {}, 'shortcut': wo, 'title': wo, 'icon': wo
        }
        fields = list(extra_kwargs.keys())
