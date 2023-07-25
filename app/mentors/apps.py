from django.apps import AppConfig

from app.base.apps import AppConfigMixin


class MentorsConfig(AppConfigMixin, AppConfig):
    name = 'app.mentors'
