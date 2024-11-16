from django.apps import AppConfig
from django.core.signals import request_finished
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from . import signals
        user_logged_in.connect(signals.redirect_after_login, sender=get_user_model())


