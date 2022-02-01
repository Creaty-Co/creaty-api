from modeltranslation.translator import register, TranslationOptions

from geo.models import *
from tags.models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ['title']


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ['name']


@register(Language)
class LanguageTranslationOptions(TranslationOptions):
    fields = ['name']
