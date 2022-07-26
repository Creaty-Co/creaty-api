from django.core.management.base import BaseCommand

from pages.models import DocumentLink
from pages.models.choices import DocumentLinkType


class Command(BaseCommand):
    DEFAULT_DOCUMENT_LINKS = {
        t: {'url': 'https://google.com'} for t in DocumentLinkType
    }
    
    def handle(self, *args, **options):
        is_reset = options.get('reset', False)
        for document_type, fields in self.DEFAULT_DOCUMENT_LINKS.items():
            document_link = DocumentLink.objects.filter(type=document_type).first()
            if document_link is None:
                document_link = DocumentLink(type=document_type)
            elif not is_reset:
                return
            for field, value in fields.items():
                setattr(document_link, field, value)
            document_link.save()

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            default=False,
            help='Установить значения по умолчанию',
        )
