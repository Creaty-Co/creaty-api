import requests
from django.core.management.base import BaseCommand

from app.pages.models import Locale


def synchronize_dicts(source_dict: dict, target_dict: dict) -> dict:
    for key, value in source_dict.items():
        if isinstance(value, dict) and isinstance(target_dict.get(key), dict):
            synchronize_dicts(value, target_dict[key])
        else:
            target_dict[key] = value
    for key in list(target_dict.keys()):
        if key not in source_dict:
            del target_dict[key]
        elif isinstance(target_dict[key], dict) and isinstance(
            source_dict.get(key), dict
        ):
            synchronize_dicts(source_dict[key], target_dict[key])
    return target_dict


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--base_url',
            type=str,
            help="Base URL for API requests to fetch translation.json",
        )
        parser.add_argument(
            '--languages',
            nargs='+',
            default=['en'],
            help="List of languages for which to update locales. Default: ['en']",
        )

    def handle(self, *args, **options):
        base_url = options['base_url']
        languages = options['languages']
        for language in languages:
            try:
                locale = Locale.objects.get(language=language)
            except Locale.DoesNotExist:
                continue
            remote_json = self._get_remote_translation_json(base_url, language)
            locale.json = synchronize_dicts(remote_json, locale.json)
            locale.save()

    def _get_remote_translation_json(self, base_url: str, language: str) -> dict:
        return requests.get(
            f"{base_url}/pages/locales/{language}/translation.json"
        ).json()
