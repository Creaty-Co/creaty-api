from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from forms.models import Field, Form
from forms.models.choices import FormField


class _FormsFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        extra_kwargs = {'type': {'help_text': choices_to_help_text(FormField)}}
        fields = ['type', 'placeholder']


class FormSerializer(serializers.ModelSerializer):
    fields = _FormsFieldsSerializer(many=True, source='field_set', write_only=True)
    
    class Meta:
        model = Form
        fields = ['description', 'post_send', 'fields']
    
    def update(self, form, validated_data):
        fields = validated_data.pop('field_set', None)
        if fields:
            for field in fields:
                field_instance = Field.objects.get(form=form, type=field['type'])
                field_instance.placeholder = field['placeholder']
                field_instance.save()
        return super().update(form, validated_data)
