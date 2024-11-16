from django.apps import AppConfig
from django.core.signals import request_finished


class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        from . import signals
        from .models import ProductCategory, Product
        request_finished.connect(
            signals.on_category_save, sender=ProductCategory)
            
        request_finished.connect(
            signals.on_product_save, sender=Product)
