from app.base.serializers.base import BaseModelSerializer
from app.base.utils.functions import choices_to_help_text
from app.pages.models import DocumentLink
from app.pages.models.choices import DocumentLinkType


class ListPagesLinksDocumentsSerializer(BaseModelSerializer):
    class Meta:
        model = DocumentLink
        extra_kwargs = {'type': {'help_text': choices_to_help_text(DocumentLinkType)}}
        fields = ['id', 'type', 'url']


class PagesLinksDocumentSerializer(BaseModelSerializer):
    class Meta:
        model = DocumentLink
        wo = {'write_only': True}
        extra_kwargs = {'url': wo}
        fields = list(extra_kwargs.keys())
