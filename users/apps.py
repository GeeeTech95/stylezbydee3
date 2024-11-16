from django.apps import AppConfig
from django.core.signals import request_finished


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self) :
        from . import signals
        from django.contrib.auth import get_user_model
        request_finished.connect(signals.create_user_credentials, sender=get_user_model())    




