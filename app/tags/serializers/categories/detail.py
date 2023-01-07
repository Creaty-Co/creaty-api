from rest_framework.validators import UniqueValidator

from app.base.serializers.base import BaseModelSerializer
from app.base.serializers.fields.image import Base64ImageField
from app.tags.models import Category, Tag


class TagsCategorySerializer(BaseModelSerializer):
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
            'title': wo,
            'icon': {},
        }
        fields = list(extra_kwargs.keys())
