from django.apps import AppConfig


class TagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.tags'

    def ready(self):
        super().ready()
        __import__(f'{self.name}.signals')
