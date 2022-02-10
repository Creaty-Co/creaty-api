from django.core.management.base import BaseCommand

from pages.models import DocumentLink
from pages.models.choices import DocumentLinkType


class Command(BaseCommand):
    DEFAULT_DOCUMENT_LINKS = {t: {'url': 'https://google.com'} for t in DocumentLinkType}
    
    def handle(self, *args, **options):
        for document_type, fields in self.DEFAULT_DOCUMENT_LINKS.items():
            document_link = DocumentLink.objects.filter(
                type=document_type
            ).first() or DocumentLink(type=document_type)
            for field, value in fields.items():
                setattr(document_link, field, value)
            document_link.save()
