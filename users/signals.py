
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.db.models import Q
from django.conf import settings
from django.core.management import call_command
from users.models import Security, Setting,CustomPermission
from core.communication import AccountMail

@receiver(post_save, sender=get_user_model())
def create_user_credentials(sender, instance, created, **kwargs):
    if created:
        # connect user to Abenity
        Security.objects.create(user=instance)
        Setting.objects.create(user=instance)

        # send credentials email
        mail = AccountMail(instance)
        mail.send_registration_email()


@receiver(post_save, sender=CustomPermission)
def dumpdata_after_save(sender, instance, created, **kwargs):
    # This signal is fired after the model is saved
    if created:  # You can modify this to trigger for updates as well
        call_command('dumpdata', 'users.User', output='custom_permissions.json')
