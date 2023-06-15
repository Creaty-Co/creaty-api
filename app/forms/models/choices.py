from typing import Type

from django.db.models import Choices, TextChoices

from app.base.utils.functions import reverse_choices


class FormType(TextChoices):
    BECOME_MENTOR = 'become_mentor', 'Become a mentor'
    CHOOSE_MENTOR = 'choose_mentor', 'Get help choosing a mentor'
    TEST_MEETING = 'test_meeting', 'Free test meeting'
    STILL_QUESTIONS = 'still_questions', 'Still have questions'


FormType: Type[str] | Type[Choices]
rFormType = reverse_choices(FormType)


class FormField(TextChoices):
    NAME = 'name', 'Name'
    EMAIL = 'email', 'Email'
    ABOUT = 'about', 'About the issue'
    LINK = 'link', 'Profile link'


FormField: Type[str] | Type[Choices]
rFormField = reverse_choices(FormField)
