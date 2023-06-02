import json

from django.conf import global_settings
from django.core.management.base import BaseCommand
from django.utils import translation
from django.utils.translation import gettext_lazy
from django_countries import countries as raw_countries

from app.geo.models import Country, Language


def _get_name(code):
    return str(gettext_lazy(dict(global_settings.LANGUAGES)[code]))


class Command(BaseCommand):
    FLAG_UNICODES_FILEPATH = 'geo/management/commands/data/flag_unicodes.json'
    LANGUAGES_FILEPATH = 'geo/management/commands/data/languages.json'

    def handle(self, *args, **options):
        self.import_countries()
        self.import_languages()

    def import_countries(self):
        flag_unicodes = json.load(open(self.FLAG_UNICODES_FILEPATH))
        countries = {country.code: country for country in Country.objects.all()}
        for code, name in dict(raw_countries).items():
            code = code.lower()
            country = countries.setdefault(code, Country(code=code))
            country.name = name
            country.flag_unicode = flag_unicodes[code]
        for country in countries.values():
            country.save()

    def import_languages(self):
        language_codes = json.load(open(self.LANGUAGES_FILEPATH))
        languages = {language.code: language for language in Language.objects.all()}
        translation.activate('en')
        for code in language_codes:
            code = code.lower()
            language = languages.setdefault(code, Language(code=code))
            language.name = _get_name(code)
            translation.activate(code)
            language.name_native = _get_name(code)
        translation.activate('en')
        for language in languages.values():
            language.save()
