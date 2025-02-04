from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from fashion.models import BespokeOrder
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.forms import inlineformset_factory
from django.contrib import messages
from fashion.models import Client, BespokeOrder, BespokeOrderStaffInfo, BespokeOrderStatusLog
from fashion.forms import BespokeOrderForm, BespokeOrderStaffInfoForm, BespokeOrderStatusLogForm

from django.views.generic import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Prefetch  # Add this import
from django.contrib.auth.mixins import LoginRequiredMixin



class BespokeOrderListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = BespokeOrder
    template_name = 'staff/bespoke_orders_list.html'
    context_object_name = 'orders'
    available_statuses = ['ALL', 'PENDING', 'IN PROGRESS', 'READY FOR DELIVERY' , 'DELIVERED', 'CANCELLED']



    def get_queryset(self):
        # Access staff info for the current user
        self.staff = self.request.user.staff

        # Filter by status if provided and valid
        status = self.kwargs.get('status', 'ALL').upper()
        if status in self.available_statuses :
            if status == "PENDING" :
                queryset =  self.model.objects.pending_orders()
            elif status == "IN PROGRESS" :
                queryset = self.model.objects.in_progress_orders()   
            elif status == "READY FOR DELIVERY" : 
                queryset = self.model.objects.ready_for_delivery_orders()
            elif status == "DELIVERED" :
                queryset = self.model.objects.delivered_orders()
            elif status == "CANCELLED" :
                queryset = self.model.objects.cancelled_orders()
            else :
                queryset = self.model.objects.all()    
        
        
        # Filter orders assigned to the current staff
        queryset = queryset.filter(staff_info__staff=self.staff)  
        
        # Prefetch related BespokeOrderStaffInfo objects for staff-specific details
        staff_info_qs = BespokeOrderStaffInfo.objects.filter(staff=self.staff)
        queryset = queryset.prefetch_related(
            Prefetch('staff_info', queryset=staff_info_qs, to_attr='staff_info_attrs')
        )
        return queryset




    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_orders_count'] = self.model.created_in_last_week(True)

        # Add available statuses for navigation
        context['available_statuses'] = ['ALL', 'PENDING',
                                         'IN PROGRESS', 'DELIVERED', 'CANCELLED']
        context['selected_status'] = self.kwargs.get('status', 'ALL').upper()

        # Retrieve staff info (including 'pay') for each order
        for order in context['orders']:
            order.staff_infos = getattr(order, 'staff_info_attrs', [])[
                0] if order.staff_info_attrs else None
        
        return context
    
    


class BespokeOrderDetailView(LoginRequiredMixin,DetailView):
    login_url = reverse_lazy('login')
    model = BespokeOrder
    template_name = 'staff/bespoke-order-detail.html'
    context_object_name = 'order'




