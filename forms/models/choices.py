from django.db.models import TextChoices

from base.utils.functions import reverse_choices


class FormType(TextChoices):
    BECOME_MENTOR = 'become_mentor', 'Станьте ментором'
    CHOOSE_MENTOR = 'choose_mentor', 'Получить помощь в подборе ментора'
    TEST_MEETING = 'test_meeting', 'Беспатная тестовая встреча'
    STILL_QUESTIONS = 'still_questions', 'Ещё остались вопросы'


ReverseFormType = reverse_choices(FormType)


class FormField(TextChoices):
    NAME = 'name', 'Имя'
    EMAIL = 'email', 'Email'
    TELEGRAM = 'telegram', 'Telegram'
    FACEBOOK = 'facebook', 'Facebook messanger'
    WHATS_APP = 'whats_app', 'WhatsApp'
    VIBER = 'viber', 'Viber'
    ABOUT = 'about', 'О себе'


ReverseFormField = reverse_choices(FormField)
