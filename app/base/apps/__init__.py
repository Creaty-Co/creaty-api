from django.apps import AppConfig

from app.base.apps.mixin import AppConfigMixin


class MainConfig(AppConfigMixin, AppConfig):
    name = 'app.base'
