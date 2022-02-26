from modeltranslation.translator import register, TranslationOptions

from forms.models import *
from geo.models import *
from mentors.models import *
from pages.models import *
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


@register(Mentor)
class MentorTranslationOptions(TranslationOptions):
    fields = ['profession', 'first_name', 'last_name']


@register(MentorInfo)
class MentorInfoTranslationOptions(TranslationOptions):
    fields = ['city', 'resume', 'what_help', 'experience', 'portfolio']


@register(Form)
class FormTranslationOptions(TranslationOptions):
    fields = ['description', 'post_send']


@register(Field)
class FieldTranslationOptions(TranslationOptions):
    fields = ['placeholder']


@register(Faq)
class FaqTranslationOptions(TranslationOptions):
    fields = ['question', 'answer']
