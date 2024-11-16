
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Shipment,StatusLog,TransitLog
from core.communication import LogisticsMail

@receiver(post_save, sender= Shipment)
def shipment_on_create(sender, instance, created, **kwargs):
    if  created :
        #send email that the shipment has been registered
        #create first status 
        StatusLog.objects.create(shipment = instance,status = "registered")
        mail = LogisticsMail(instance)
        mail.send_shipment_created_mail()
        
           
  
@receiver(post_save, sender= TransitLog)
def shipment_on_transit_update(sender, instance, created, **kwargs):
    if  created :
        #send email that the shipment has been updated
        mail = LogisticsMail(instance.shipment)
        mail.send_shipment_progress_mail()
        
               
    
@receiver(post_save, sender= StatusLog)
def shipment_on_status_update(sender, instance, created, **kwargs):
    if  created :
        #send email that the shipment has been updated
        mail = LogisticsMail(instance.shipment)
        mail.send_shipment_progress_mail()
        
            

