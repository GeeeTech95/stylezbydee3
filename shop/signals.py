
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import ProductCategory


@receiver(post_save, sender=ProductCategory)
def on_category_save(sender, instance, created, **kwargs):

    if created:
        # saving now with  pk adds pk to slug to make it unique
        instance.slug = instance.generate_slug()
        instance.save()


@receiver(post_save, sender=ProductCategory)
def on_product_save(sender, instance, created, **kwargs):

    if created:
        instance.slug = instance.generate_slug()
        instance.save()
