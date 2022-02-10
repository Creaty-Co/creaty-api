from rest_framework import serializers

from base.utils.functions import choices_to_help_text
from pages.models import DocumentLink
from pages.models.choices import DocumentLinkType


class ListPagesLinksDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLink
        extra_kwargs = {'type': {'help_text': choices_to_help_text(DocumentLinkType)}}
        fields = ['id', 'type', 'url']


class PagesLinksDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentLink
        wo = {'write_only': True}
        extra_kwargs = {'id': {}, 'url': wo}
        fields = list(extra_kwargs.keys())
