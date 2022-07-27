import json

from django.conf import settings
from django.core.management.base import BaseCommand

from pages.models import Locale


class Command(BaseCommand):
    DEFAULT_JSON_FILES = {
        'ru': 'pages/management/commands/default_ru.json',
        'en': 'pages/management/commands/default_en.json',
    }

    def handle(self, *args, **options):
        is_reset = options.get('reset', False)
        for language, _ in settings.LANGUAGES:
            locale = Locale.objects.filter(language=language).first()
            if locale is None:
                locale = Locale(language=language)
            elif not is_reset:
                return
            with open(self.DEFAULT_JSON_FILES[language], 'r') as default_json:
                locale.json = json.load(default_json)
            locale.save()

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            default=False,
            help='Установить значения по умолчанию',
        )
