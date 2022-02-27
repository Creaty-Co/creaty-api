from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from tags.models import Category, Tag


class TagsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        wo = {'write_only': True}
        extra_kwargs = {
            'id': {}, 'shortcut': wo | {
                'validators': [
                    UniqueValidator(Tag.objects.all()),
                    UniqueValidator(Category.objects.all())
                ]
            }, 'title': wo, 'icon': wo
        }
        fields = list(extra_kwargs.keys())
