from django.core.management.base import BaseCommand

from pages.services.page import PageService


class Command(BaseCommand):
    def handle(self, *args, **options):
        _ = PageService.main
