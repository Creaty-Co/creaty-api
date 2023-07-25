from django.apps import AppConfig

from app.base.apps import AppConfigMixin


class TagsConfig(AppConfigMixin, AppConfig):
    name = 'app.tags'
