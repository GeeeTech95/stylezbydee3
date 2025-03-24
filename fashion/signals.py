
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Q
from django.conf import settings
from .models import BespokeOrder, BespokeOrderStatusLog
from .models import ClientBodyMeasurement,Client,Measurement,BespokeOrderStaffInfo
from core.communication import FashionNotification


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
    if hasattr(instance.client, "measurement"):
        #check if measurement log has been created before 
        # Create a status log entry if the client has a saved measurement
        log,_created =  BespokeOrderStatusLog.objects.get_or_create(
            outfit=instance,
            status=BespokeOrderStatusLog.MEASUREMENT_ACQUIRED,
        )
    else:
        # Log a message if no measurement is found
        print(f"No measurements found for client {instance.client.full_name}.")




@receiver(post_save, sender=BespokeOrderStaffInfo)
def send_staff_assignment_notification(sender, instance, created, **kwargs):
    """
    Sends an SMS and WhatsApp message to staff when they are assigned a BespokeOrder.
    """
    if created:  # Ensure the notification is only sent when a new record is created
        staff = instance.staff
        order = instance.order
        message = f"Dear {staff}, you have been assigned to Order #{order.order_id}. " \
                  f"Delegation: {instance.get_delegation_display()}. Please check your dashboard for details."
        
        notify = FashionNotification()
        notify.send_staff_order_notification(message)
