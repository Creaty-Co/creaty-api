from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from forms.models import Field, Form
from forms.models.choices import FormField


class _FormsFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        extra_kwargs = {
    'type': {'help_text': choices_to_help_text(FormField)},
    'placeholder': {'allow_blank': True},
}
        fields = ['type', 'placeholder']


class FormSerializer(serializers.ModelSerializer):
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
