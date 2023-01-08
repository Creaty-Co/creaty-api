from django.core.management.base import BaseCommand

from app.forms.models import Field, Form
from app.forms.models.choices import FormField, FormType

_default_post_send_ru = 'Мы в ближайшее время свяжемся с вами, чтобы обсудить детали!'
_default_post_send_en = 'We will contact you soon to discuss the details!'
_default_field_set = [
    {'type': FormField.NAME, 'placeholder_ru': 'Имя', 'placeholder_en': 'Name'},
    {'type': FormField.EMAIL, 'placeholder_ru': 'Email', 'placeholder_en': 'Email'},
    {
        'type': FormField.TELEGRAM,
        'placeholder_ru': 'Номер или ник в ',
        'placeholder_en': 'Number or nickname in ',
    },
    {
        'type': FormField.FACEBOOK,
        'placeholder_ru': 'Номер или ник в ',
        'placeholder_en': 'Number or nickname in ',
    },
    {
        'type': FormField.WHATS_APP,
        'placeholder_ru': 'Номер или ник в ',
        'placeholder_en': 'Number or nickname in ',
    },
    {
        'type': FormField.VIBER,
        'placeholder_ru': 'Номер или ник в ',
        'placeholder_en': 'Number or nickname in ',
    },
]


class Command(BaseCommand):
    DEFAULT_FORMS = {
        FormType.BECOME_MENTOR: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder_ru': (
                        'Расскажите кратко о себе!\nМожно поделиться ' 'позже :)'
                    ),
                    'placeholder_en': (
                        'Tell us briefly about yourself!\nYou can share '
                        ''
                        'it later :)'
                    ),
                }
            ],
        },
        FormType.CHOOSE_MENTOR: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder_ru': (
                        'С чем требуется помощь ментора?\nМожно обсудить ' '' 'позже :)'
                    ),
                    'placeholder_en': (
                        'What does a mentor need help with?\nWe can '
                        'discuss it later :)'
                    ),
                }
            ],
        },
        FormType.TEST_MEETING: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder_ru': (
                        'С чем требуется помощь ментора?\nМожно обсудить '
                        ''
                        ''
                        'позже :)'
                    ),
                    'placeholder_en': (
                        'What does a mentor need help with?\nWe can '
                        'discuss it later :)'
                    ),
                }
            ],
        },
        FormType.STILL_QUESTIONS: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'field_set': _default_field_set,
        },
        FormType.SIGNUP_MENTOR: {
            'post_send_ru': _default_post_send_ru,
            'post_send_en': _default_post_send_en,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder_ru': (
                        'С чем требуется помощь ментора?\nМожно обсудить '
                        ''
                        ''
                        'позже :)'
                    ),
                    'placeholder_en': (
                        'What does a mentor need help with?\nWe can '
                        'discuss it later :)'
                    ),
                }
            ],
        },
    }

    def handle(self, *args, **options):
        is_reset = options.get('reset', False)
        for form_type, fields in self.DEFAULT_FORMS.items():
            form = Form.objects.filter(type=form_type).first()
            if form is None:
                form = Form(type=form_type)
            elif not is_reset:
                return
            field_set = fields.pop('field_set')
            for field, value in fields.items():
                setattr(form, field, value)
            form.save()
            for field_data in field_set:
                field_instance = Field.objects.filter(
                    type=field_data['type'], form=form
                ).first() or Field(form=form)
                for f, v in field_data.items():
                    setattr(field_instance, f, v)
                field_instance.save()

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            default=False,
            help='Установить значения по умолчанию',
        )
