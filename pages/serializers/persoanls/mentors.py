from django.db.models import Max
from rest_framework import serializers, status

from base.exceptions import APIWarning
from base.schemas.mixins import SerializerSchemaMixin
from base.serializers.base import BaseSerializer
from mentors.models import Mentor
from pages.models import PageMentorSet


class UpdatePagesPersonalMentorsSerializer(SerializerSchemaMixin, BaseSerializer):
    WARNINGS = {
        409: APIWarning(
            'max_page_mentor_index',
            'Превышено максимальное количество менторов, прикреплённых к странице',
            status.HTTP_409_CONFLICT
        )
    }
    
    mentor = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Mentor.objects.all()
    )
    id = serializers.IntegerField(read_only=True)
