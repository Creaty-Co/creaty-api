from app.base.serializers.base import BaseModelSerializer
from app.base.utils.functions import choices_to_help_text
from app.forms.models import Field, Form
from app.forms.models.choices import FormField


class _FormsFieldsSerializer(BaseModelSerializer):
    class Meta:
        model = Field
        extra_kwargs = {
            'type': {'help_text': choices_to_help_text(FormField)},
            'placeholder': {'allow_blank': True},
        }
        fields = ['type', 'placeholder']


class FormSerializer(BaseModelSerializer):
    fields = _FormsFieldsSerializer(many=True, source='field_set', write_only=True)

    class Meta:
        model = Form
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'description': wo, 'post_send': wo, 'fields': {}}
        fields = list(extra_kwargs.keys())

    def update(self, form, validated_data):
        fields = validated_data.pop('field_set', None)
        if fields:
            for field in fields:
                field_instance = Field.objects.get(form=form, type=field['type'])
                if field['placeholder']:
                    field_instance.placeholder = field['placeholder']
                    field_instance.save()
                else:
                    field_instance.delete()
        return super().update(form, validated_data)
