from modeltranslation.translator import register, TranslationOptions

from forms.models import *
from geo.models import *
from mentors.models import *
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


@register(MentorInfo)
class MentorInfoTranslationOptions(TranslationOptions):
    fields = ['city']


@register(Form)
class FormTranslationOptions(TranslationOptions):
    fields = ['description', 'post_send']
