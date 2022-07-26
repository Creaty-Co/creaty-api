from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from tags.models import Category, Tag


class UpdateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {},
            'shortcut': wo
            | {
                'validators': [
                    UniqueValidator(Tag.objects.all()),
                    UniqueValidator(Category.objects.all()),
                ]
            },
            'title': wo,
        }
        fields = list(extra_kwargs.keys())
