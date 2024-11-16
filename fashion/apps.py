from django.apps import AppConfig

class FashionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fashion'

    def ready(self):
        # Import the signals module to ensure that the signal handlers are connected
        import fashion.signals  # Replace with the correct path to your signals module
        