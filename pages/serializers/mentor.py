from rest_framework import serializers, status

from base.exceptions import APIWarning
from base.schemas.mixins import SerializerSchemaMixin
from base.serializers.base import BaseSerializer


class UpdatePageMentorSerializer(SerializerSchemaMixin, BaseSerializer):
    WARNINGS = {
        409: APIWarning(
            'max_page_mentor_index',
            'Превышено максимальное количество менторов, прикреплённых к странице',
            status.HTTP_409_CONFLICT
        )
    }
    
    id = serializers.IntegerField(read_only=True)
