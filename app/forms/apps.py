from django.apps import AppConfig


class FormsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.forms'

    def ready(self):
        super().ready()
        __import__(f'{self.name}.signals')
