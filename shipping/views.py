from django.shortcuts import render,get_object_or_404

from django.views.generic import View,DetailView
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.urls import reverse

from logistics.models import Shipment

from myadmin.forms import StatusLogForm, TransitLogForm
import time



class TrackShipment(View) :

    def get(self,request,*args,**kwargs) :
        feedback = {}
        time.sleep(2)
        tracking_number = request.GET.get("tracking_number")
        if not tracking_number :
            feedback['error'] = "Invalid request, a tracking number is expected"

        else :
            feedback['success'] = True
            feedback['success_url'] = reverse("shipment-detail",args=[tracking_number.strip()])
        
        return JsonResponse(feedback)
  



class ShipmentDetail(View) :
    model = Shipment
    context_object_name = "shipment"

    def get_template_name(self) :
        return "shipment-detail.html"    


    def get(self,request,*args,**kwargs) :
        shipment = self.model.objects.filter(tracking_number = kwargs['tracking_number'])
        
        if shipment.exists() :
            self.shipment = shipment.first()
            ctx = self.get_context_data(**kwargs)
            ctx['shipment'] = self.shipment
            return render(request,self.get_template_name(),locals())

        else :
            return HttpResponse("The entered tracking number is incorrect, No shipment with the tracking number was found")   
    
    def get_context_data(self,**kwargs) :
        ctx = {}
        ctx['timeline'] = self.shipment.timeline_logs
        ctx['status_log_form']  =   StatusLogForm()
        ctx['transit_log_form']  =   TransitLogForm()
        return ctx


