from django.core.management.base import BaseCommand

from app.forms.management.commands import create_forms
from app.geo.management.commands import import_geo
from app.pages.management.commands import create_document_links, create_locales


class Command(BaseCommand):
    COMMANDS = [import_geo]
    RESET_COMMANDS = [create_forms, create_document_links, create_locales]

    def handle(self, *args, **options):
        for command in self.COMMANDS:
            command.Command().handle()
        for command in self.RESET_COMMANDS:
            command.Command().handle(reset=True)
