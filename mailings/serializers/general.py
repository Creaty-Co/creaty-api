from celery.result import AsyncResult
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from mailings.models import Mailing


class MailingsListSerializer(serializers.ModelSerializer):
    is_done = serializers.SerializerMethodField(
        allow_null=True,
        help_text='true — выполнено\n\nfalse — выполняется\n\nnull — ещё не выполнялось'
    )
    
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_done(self, mailing):
        if mailing.task_ids is None:
            return None
        for task_id in mailing.task_ids:
            if AsyncResult(task_id).state in ('SENT', 'STARTED', 'RETRY'):
                return False
        return True
    
    class Meta:
        model = Mailing
        fields = ['id', 'subject', 'is_done']


class MailingsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'subject': wo, 'content': wo}
        fields = list(extra_kwargs.keys())
