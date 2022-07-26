from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from pages.serializers.main import (
    PagesRetrieveMainSerializer,
    PagesUpdateMainSerializer,
)


class PagesRetrievePersonalSerializer(PagesRetrieveMainSerializer):
    title = serializers.SerializerMethodField(allow_null=True)

    class Meta(PagesRetrieveMainSerializer.Meta):
        fields = PagesRetrieveMainSerializer.Meta.fields[:]
        fields.insert(1, 'title')

    @extend_schema_field(OpenApiTypes.STR)
    def get_title(self, page):
        if page.tag is None:
            if page.category is None:
                return None
            return page.category.title
        return page.tag.title


class PagesUpdatePersonalSerializer(PagesUpdateMainSerializer):
    pass
