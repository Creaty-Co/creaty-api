from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.base.serializers.base import BaseModelSerializer
from app.tags.models import Category, Tag


class ListTagsSerializer(BaseModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'shortcut', 'title']


class POSTTagsSerializer(BaseModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, allow_empty=False
    )

    class Meta:
        model = Tag
        extra_kwargs = {
            'shortcut': {
                'validators': [
                    UniqueValidator(Tag.objects.all()),
                    UniqueValidator(Category.objects.all()),
                ]
            }
        }
        write_only_fields = ['shortcut', 'title', 'categories']
