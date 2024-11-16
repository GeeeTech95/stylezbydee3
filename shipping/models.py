from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import uuid
import re

from core.models import Country


class Station(models.Model) :
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    country = models.ForeignKey(Country, related_name = 'stations',on_delete = models.CASCADE)



class Shipment(models.Model) :


    def get_tracking_number() :
        tracking_number =  ''.join(filter(str.isdigit,str(uuid.uuid4())))
        return tracking_number[:8]
    
   
    tracking_number = models.CharField(default= get_tracking_number, max_length=8,blank = True)
    is_paid = models.BooleanField(default=False,blank = True)
    shipment_fee = models.DecimalField(decimal_places=2,max_digits=100,help_text = "in dollars($)")


    date = models.DateTimeField(auto_now_add = True)
    _estimated_arrival_date = models.DateTimeField(null=True,blank=True)
    _estimated_departure_date = models.DateTimeField( blank=True,null=True)


    @property
    def fragility(self) :
        return "YES" if self.is_fragile else "NO"
    
    @property
    def origin(self) :
        return "{}, {}".format(self.source_address,self.source_country)
    
    @property
    def destination(self) :
        return "{}, {}".format(self.destination_address,self.destination_country)
    
    @property
    def estimated_arrival_date(self) :
        return self._estimated_arrival_date or self._estimated_arrival_date  +  timezone.timedelta(weeks=3)
    
     
    @property
    def estimated_departure_date(self) :
        return self._estimated_departure_date or self.date  +  timezone.timedelta(days=2)
 

    def __str__(self) :
        return self.tracking_number

    def save(self,*args,**kwargs) :
        super(Shipment,self).save(*args,**kwargs)

    def update_status_log(self,date = None)   :
        statuses = [value for name,value in StatusLog.StatusChoices]
        current_status = self.last_status_log.status
        #update to next
        #get current index 
        _index = statuses.index(current_status) 
        if _index < len(statuses) - 1 :
            #anything above means its already in transit then we do nothing
            StatusLog.objects.create(shipment = self,status = statuses[_index + 1],date = date)
        else : 
            return "You cannot update status log any further, shipment is already in {}".format(current_status)  #meaning error     
       

    def roll_back_status_log(self) :
        statuses = [value for name,value in StatusLog.StatusChoices]
        current_status = self.last_status_log.status
        #update to next
        #get current index 
        _index = statuses.index(current_status) 
        if _index > 0 :
            #anything below 1 means its already in transit in the beigining, we cannot roll back further]
            #delete last log
            self.last_status_log.delete()
        else : 
            return "You cannot roll back status log any further, shipment is in {} status".format(current_status)  #meaning error  
    
    def roll_back_transit_log(self) :

        #delete transit last log
        if self.last_transit_log :
            self.last_transit_log.delete()

        else : 
            self.roll_back_status_log()

    @property
    def payment_status(self) :
        if self.is_paid : return "PAID"   
        else : return "NOT PAID"        

    @property
    def registration_date(self) :
        try :
            return self.status_logs.filter(status = "registered").first().date 
        except :
            return       
    

    @property
    def is_in_transit(self) :
        if self.last_status_log.status == "in transit" : return True
        return False


    @property
    def timeline_logs(self) :
        status_logs = self.status_logs.order_by("date")
        try : transit_logs = self.transit_logs.order_by("date")  
        except ObjectDoesNotExist : transit_logs = None
       
        #combine
        timeline = []
        for log in status_logs :
            logs = {}
            logs['date'] = log.date
            logs['status'] = log.status_verbose
            timeline.append(logs)

        if transit_logs :  
            for log in transit_logs : 
                logs = {}
                logs['date'] = log.date
                logs['status'] = log.status_verbose
                timeline.append(logs)

        return timeline    

    @property
    def last_status_log(self) :
        return self.status_logs.all()[0]

    @property
    def last_transit_log(self) :
        try : 
            return self.transit_logs.all()[0]
        except (ObjectDoesNotExist,IndexError) : 
            return    

    @property
    def shipment_status_log(self)  :
        if self.last_status_log.status != "in transit" :
            log = {
            "location" : "packaging station",
            "status" : self.last_status_log.status,
            "date_since" : self.last_status_log.date,
            "status_verbose" : self.last_status_log.status,
        }

        else :
            #then get transit data
            current_transit_log = self.last_transit_log
            if current_transit_log :
                log = {
                "location" : "{} station".format(current_transit_log.station),
                "status" : self.last_transit_log.status,
                "date_since" : self.last_transit_log.date,
                "status_verbose" : self.last_transit_log.status_verbose,
                }

            else :
                log = {}    

        return log



class StatusLog(models.Model) :
    initial_terminal_name = "Collecting"
    
    StatusChoices = (
        ("registered","registered"),
        ("received","received"),
        ("processing","processing"),
        ("in transit","in transit")

    )

    shipment = models.ForeignKey(Shipment,related_name = "status_logs",on_delete = models.CASCADE)
    status  = models.CharField(max_length = 10,choices = StatusChoices)
    date = models.DateTimeField() #editable

    def __str__(self) :
        return "{} - {}".format(self.shipment,self.status)

    class Meta() :
        ordering = ['-date']

    def save(self,*args,**kwargs) :
        if self.status == "in transit" :
            #make sure a shipment log has been created for this shipment
            #if not raise an Object Does not Exists exception and prevent save
            _ = self.shipment.transit_logs

        if not self.date : self.date = timezone.now()  
        #send email
          
        super(StatusLog,self).save(*args,**kwargs) 
    
    @property
    def status_verbose(self) :
        if self.status == "registered" :
            return "Package has just been registered, but not yet received at initial terminal".format(self.initial_terminal_name)
        
        elif self.status == "received" :
            return "Package has been received at {} terminal, awaiting processing.".format(self.initial_terminal_name)
        
        elif self.status == "processing" :
            return "Package is been processed at {} terminal".format(self.initial_terminal_name)

        else :
            return "Package has left {} terminal and is now in transit".format(self.initial_terminal_name)


class TransitLog(models.Model) :

    StatusChoices = (
        ("arrived","arrived"),
        ("processing","processing"),
        ("dispatched","dispatched")

    )
    shipment = models.ForeignKey(Shipment,related_name = 'transit_logs',on_delete = models.CASCADE)
    status  = models.CharField(max_length = 10,choices = StatusChoices)
    #station = models.ForeignKey(Station,on_delete = models.CASCADE,related_name ="transit_logs")
    station = models.CharField(max_length=30)
    date = models.DateTimeField()  #editable


    def __str__(self) :
        if self.status == "arrived" :
            return "shipment {}, arrived at station-{} on {}".format(self.shipment,self.station,self.date.strftime("%d %b, %Y. %I:%M %p"))
        
        elif self.status == "proccessing" :
            return "shipment {}, processed at station-{} on {}".format(self.shipment,self.station,self.date.strftime("%d %b, %Y. %I:%M %p"))
        
        else :
            return "shipment {}, dispatched from station-{} on {}".format(self.shipment,self.station,self.date.strftime("%d %b, %Y. %I:%M %p"))



    def save(self,*args,**kwargs) :
        if not self.date : self.date = timezone.now()  
        super(TransitLog,self).save(*args,**kwargs)

    @property
    def status_verbose(self) :
        if self.status == "arrived" :
            return "Package has arrived at {} terminal, awaiting processing".format(self.station)

        elif self.status == "processing" :
            return "Package is being processed at {} terminal".format(self.station)  

        else : return "Package has left {}, and now been dispatched to the next terminal".format(self.station)    


    class Meta() :
        ordering = ['-date']
