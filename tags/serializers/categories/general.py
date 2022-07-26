from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from base.serializers.fields.image import Base64ImageField
from tags.models import Category, Tag
from tags.serializers.general import ListTagsSerializer


class ListTagsCategoriesSerializer(serializers.ModelSerializer):
    tags = ListTagsSerializer(many=True, source='tag_set')

    class Meta:
        model = Category
        fields = ['id', 'shortcut', 'title', 'icon', 'tags']


class CreateTagsCategoriesSerializer(serializers.ModelSerializer):
    icon = Base64ImageField(write_only=True)

    class Meta:
        model = Category
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
    'title_ru': wo,
    'title_en': wo,
    'icon': {},
}
        fields = list(extra_kwargs.keys())
