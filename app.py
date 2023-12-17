from django.apps import AppConfig
from .thread import ClockThread


class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'

    def ready(self):
        ClockThread().start()
