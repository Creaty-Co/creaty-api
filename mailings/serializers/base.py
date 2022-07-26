from celery.result import AsyncResult
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from mailings.models import Mailing


class BaseMailingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing

    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_running(self, mailing):
        if mailing.is_stopped:
            return False
        if mailing.task_ids:
            for task_id in mailing.task_ids:
                if AsyncResult(task_id).status in ('SENT', 'STARTED', 'RETRY'):
                    return True
        return False
