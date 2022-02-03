from rest_framework import serializers

from base.utils import choices_to_help_text
from forms.models import Form
from forms.models.choices import *


class FormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Form
        extra_kwargs = {
            'type': {'help_text': choices_to_help_text(FormType)},
            'fields': {'help_text': choices_to_help_text(FormField)}
        }
        fields = ['id', 'type', 'description', 'post_send', 'fields']
