from django.apps import AppConfig


class PagesConfig(AppConfig):
    name = 'pages'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        from . import signals

