from django.core.management.base import BaseCommand

from app.forms.models import Field, Form
from app.forms.models.choices import FormField, FormType

_default_post_send = 'We will contact you soon to discuss the details!'
_default_field_set = [
    {'type': FormField.NAME, 'placeholder': 'Name'},
    {'type': FormField.EMAIL, 'placeholder': 'Email'},
]


class Command(BaseCommand):
    DEFAULT_FORMS = {
        FormType.BECOME_MENTOR: {
            'post_send': _default_post_send,
            'field_set': _default_field_set
            + [
                {'type': FormField.LINK, 'placeholder': 'Link on the profile '},
                {
                    'type': FormField.ABOUT,
                    'placeholder': (
                        'Tell us briefly about yourself!\nYou can share ' 'it later :)'
                    ),
                },
            ],
        },
        FormType.CHOOSE_MENTOR: {
            'post_send': _default_post_send,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder': (
                        'What does a mentor need help with?\nWe can '
                        'discuss it later :)'
                    ),
                }
            ],
        },
        FormType.TEST_MEETING: {
            'post_send': _default_post_send,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder': (
                        'What does a mentor need help with?\nWe can '
                        'discuss it later :)'
                    ),
                }
            ],
        },
        FormType.STILL_QUESTIONS: {
            'post_send': _default_post_send,
            'field_set': _default_field_set,
        },
        FormType.SIGNUP_MENTOR: {
            'post_send': _default_post_send,
            'field_set': _default_field_set
            + [
                {
                    'type': FormField.ABOUT,
                    'placeholder': (
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
            help='Set default values',
        )
