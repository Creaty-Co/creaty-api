from typing import Type

from django.db.models import Choices, TextChoices


class DocumentLinkType(TextChoices):
    FACEBOOK = 'facebook', 'Facebook'
    INSTAGRAM = 'instagram', 'Instagram'
    HELP = 'help', 'Написать в поддержку'
    USER_AGREEMENT = 'user_agreement', 'Пользовательское соглашение'
    PRIVACY_POLICY = 'privacy_policy', 'Политика конфиденциальности'
    COOKIE_POLICY = 'cookie_policy', 'Cookie Policy'


DocumentLinkType: Type[str] | Type[Choices]
