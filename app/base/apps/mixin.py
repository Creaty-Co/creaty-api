from django.apps import AppConfig


class AppConfigMixin:
    name: str
    default_auto_field: str = 'django.db.models.BigAutoField'

    def ready(self):
        assert isinstance(self, AppConfig)
        AppConfig.ready(self)
        try:
            __import__(f"{self.name}.signals")
        except ImportError:
            pass
