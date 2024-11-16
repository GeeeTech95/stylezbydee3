
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from django.conf import settings
from .models import BespokeOrder, BespokeOrderStatusLog
from .models import ClientBodyMeasurement,Client,Measurement


@receiver(post_save, sender=Client)
def create_user_credentials(sender, instance, created, **kwargs):
    if created:
        # create instance
        ClientBodyMeasurement.objects.create(client = instance)
     
        #send welcome emails and other credentials





@receiver(post_save, sender=BespokeOrder)
def create_initial_status_log(sender, instance, created, **kwargs):
    if created:
        # Create the first status log entry with default status "ORDER_CREATED"
        BespokeOrderStatusLog.objects.create(
            outfit=instance,
            status=BespokeOrderStatusLog.ORDER_CREATED,
        )

        # Check if the client has a saved measurement
        try:
            instance.client.measurement
            # Create a MeasurementLog if the client has a saved measurement
            BespokeOrderStatusLog.objects.create(
            outfit=instance,
            status=BespokeOrderStatusLog.MEASUREMENT_ACQUIRED,
        )
        except Measurement.DoesNotExist:
            # Client doesn't have a measurement saved, do nothing or log a message
            print(f"No measurements found for client {instance.client.full_name}.")
