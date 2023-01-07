from django.core.management.base import BaseCommand

from app.forms.management.commands import create_forms
from app.geo.management.commands import import_geo
from app.pages.management.commands import create_document_links


class Command(BaseCommand):
    COMMANDS = [import_geo, create_forms, create_document_links]

    def handle(self, *args, **options):
        for command in self.COMMANDS:
            command.Command().handle()
