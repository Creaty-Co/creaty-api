from django.core.management.base import BaseCommand

from forms.models import *
from forms.models.choices import *

_default_post_send_ru = 'Мы в ближайшее время свяжемся с вами, чтобы осбудить детали!'
_default_post_send_en = 'We will contact you soon to discuss the details!'


class Command(BaseCommand):
    DEFAULT_FORMS = {
        FormType.BECOME_MENTOR: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'fields': [
                FormField.NAME, FormField.EMAIL, FormField.TELEGRAM, FormField.FACEBOOK,
                FormField.WHATS_APP, FormField.VIBER, FormField.ABOUT
            ]
        },
        FormType.CHOOSE_MENTOR: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'fields': [
                FormField.NAME, FormField.EMAIL, FormField.TELEGRAM, FormField.FACEBOOK,
                FormField.WHATS_APP, FormField.VIBER, FormField.ABOUT
            ]
        },
        FormType.TEST_MEETING: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'fields': [
                FormField.NAME, FormField.EMAIL, FormField.TELEGRAM, FormField.FACEBOOK,
                FormField.WHATS_APP, FormField.VIBER, FormField.ABOUT
            ]
        },
        FormType.STILL_QUESTIONS: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'fields': [
                FormField.NAME, FormField.EMAIL, FormField.TELEGRAM, FormField.FACEBOOK,
                FormField.WHATS_APP, FormField.VIBER, FormField.ABOUT
            ]
        }
    }
    
    def handle(self, *args, **options):
        for form_type, fields in self.DEFAULT_FORMS.items():
            form = Form.objects.filter(type=form_type).first() or Form(type=form_type)
            for field, value in fields.items():
                setattr(form, field, value)
            form.save()
