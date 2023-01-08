from rest_framework import serializers, status

from app.base.exceptions import APIWarning
from app.base.serializers.base import BaseSerializer


class UpdatePageMentorSerializer(BaseSerializer):
    WARNINGS = {
        409: APIWarning(
            'Превышено максимальное количество менторов, прикреплённых к странице',
            status.HTTP_409_CONFLICT,
            'max_page_mentor_index',
        )
    }

    id = serializers.IntegerField(read_only=True)
