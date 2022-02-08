from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from forms.models import Form
from forms.models import Field
from forms.models.choices import *


class _FormsFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        extra_kwargs = {'type': choices_to_help_text(FormField)}
        fields = ['type', 'placeholder']


class FormsSerializer(serializers.ModelSerializer):
    fields = _FormsFieldsSerializer(many=True, source='field_set')
    
    class Meta:
        model = Form
        extra_kwargs = {'type': {'help_text': choices_to_help_text(FormType)}}
        fields = ['id', 'type', 'description', 'post_send', 'fields']
