from app.base.serializers.base import BaseModelSerializer
from app.base.utils.functions import choices_to_help_text
from app.forms.models import Field, Form
from app.forms.models.choices import FormField, FormType


class _FormsFieldsSerializer(BaseModelSerializer):
    class Meta:
        model = Field
        extra_kwargs = {'type': {'help_text': choices_to_help_text(FormField)}}
        fields = ['type', 'placeholder']


class FormsSerializer(BaseModelSerializer):
    fields = _FormsFieldsSerializer(many=True, source='field_set')

    class Meta:
        model = Form
        extra_kwargs = {'type': {'help_text': choices_to_help_text(FormType)}}
        fields = ['id', 'type', 'description', 'post_send', 'fields']
