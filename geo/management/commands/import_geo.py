import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from django_countries import countries as raw_countries

from geo.models import *


class Command(BaseCommand):
    FLAG_UNICODES_FILEPATH = 'geo/management/commands/data/flag_unicodes.json'
    LANGUAGES_FILEPATH = 'geo/management/commands/data/languages.json'
    
    def handle(self, *args, **options):
        self.import_countries()
    
    def import_countries(self):
        flag_unicodes = json.load(open(self.FLAG_UNICODES_FILEPATH))
        countries = {country.code: country for country in Country.objects.all()}
        for language, _ in settings.LANGUAGES:
            translation.activate(language)
            for code, name in dict(raw_countries).items():
                code = code.lower()
                country = countries.setdefault(code, Country(code=code))
                setattr(country, f'name_{language}', name)
                country.flag_unicode = flag_unicodes[code]
        for country in countries.values():
            country.save()
    
    # def import_languages(self):
    #     most_speakers_languages = json.load(open(self.LANGUAGES_FILEPATH))
    #     languages = {country.code: country for country in Country.objects.all()}
    #     for language, _ in settings.LANGUAGES:
    #         translation.activate(language)
    #         for code, name in dict(raw_countries).items():
    #             code = code.lower()
    #             country = countries.setdefault(code, Country(code=code))
    #             setattr(country, f'name_{language}', name)
    #             country.flag_unicode = flag_unicodes[code]
    #     for country in countries.values():
    #         country.save()
