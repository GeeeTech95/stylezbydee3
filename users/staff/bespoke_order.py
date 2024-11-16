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


class BespokeOrderListView(ListView):
    model = BespokeOrder
    template_name = 'staff/bespoke_orders_list.html'
    context_object_name = 'orders'



    def get_queryset(self):
        # Access staff info for the current user
        self.staff = self.request.user.staff

        # Base queryset for BespokeOrder filtered by the staff
        base_queryset = self.model.objects.filter(staff=self.staff)

        # Prefetch related BespokeOrderStaffInfo objects for staff-specific details
        staff_info_qs = BespokeOrderStaffInfo.objects.filter(staff=self.staff)
        queryset = base_queryset.prefetch_related(
            Prefetch('staff_info', queryset=staff_info_qs, to_attr='staff_info_attrs')
        )

        # Exclude specific statuses
        """excluded_statuses = [
            BespokeOrderStatusLog.ORDER_CREATED,
            BespokeOrderStatusLog.MEASUREMENT_ACQUIRED,
        ]
        queryset = queryset.exclude(status_log__status__in=excluded_statuses)"""

        # Filter by status if provided and valid
        status = self.kwargs.get('status', 'ALL').upper()
        valid_statuses = ['PENDING', 'DELIVERED', 'IN_PROGRESS', 'CANCELLED']
        if status in valid_statuses:
            queryset = queryset.filter(status_log__status=status)

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
    
    


class BespokeOrderDetailView(DetailView):
    model = BespokeOrder
    template_name = 'bespoke_orders/bespoke_orders_detail.html'
    context_object_name = 'order'


# Define the inline formset
BespokeOrderStaffInfoFormSet = inlineformset_factory(
    BespokeOrder, BespokeOrderStaffInfo, form=BespokeOrderStaffInfoForm, extra=1, can_delete=True
)


class BespokeOrderCreateView(CreateView):
    model = BespokeOrder
    form_class = BespokeOrderForm
    template_name = 'bespoke_orders/bespoke_order_form.html'

    def get_success_url(self):
        return reverse('myadmin:bespoke-orders-detail', args=[self.kwargs['pk']])

    def get_client(self):
        return get_object_or_404(Client, pk=self.kwargs['client_pk'])

    def get_context_data(self, **kwargs):
        # Get the context from the superclass
        context = super().get_context_data(**kwargs)
        print("obnjkect", self.object)
        # Initialize the staff formset
        if self.request.POST:
            context['staff_info_formset'] = BespokeOrderStaffInfoFormSet(
                self.request.POST, instance=self.object)
        else:

            context['staff_info_formset'] = BespokeOrderStaffInfoFormSet(
                instance=self.object)

        return context

    def form_invalid(self, form):
        # Handle invalid form submission and ensure the formset is also passed to the context
        context = self.get_context_data(form=form)

        # Debugging errors
        print("Form errors:", form.errors)
        staff_info_formset = context.get('staff_info_formset')
        print("Staff info formset errors:", staff_info_formset.errors)

        # Display a message and return the formset with errors re-rendered
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(context)

    def form_valid(self, form):
        # Ensure form and formset are valid, save them if they are
        context = self.get_context_data()
        staff_info_formset = context['staff_info_formset']

        if form.is_valid() and staff_info_formset.is_valid():
            # Save main form to get `BespokeOrder` instance
            self.object = form.save(commit=False)
            self.object.client = self.get_client()
            self.object.save()
            # Associate formset with the `BespokeOrder` instance
            staff_info_formset.instance = self.object
            staff_info_formset.save()

            messages.success(
                self.request, "Bespoke order for {} and related staff info saved successfully!".format(self.get_client()))
            return redirect(self.get_success_url())
        else:
            # If form or formsets are invalid, re-render the form with errors
            messages.error(self.request, "Please correct the errors below.")
            return self.form_invalid(form)


# Define the inline formset
BespokeOrderStaffInfoFormSet = inlineformset_factory(
    BespokeOrder, BespokeOrderStaffInfo, form=BespokeOrderStaffInfoForm, extra=0, can_delete=True
)


class BespokeOrderUpdateView(UpdateView):
    model = BespokeOrder
    form_class = BespokeOrderForm
    template_name = 'bespoke_orders/bespoke_order_form.html'

    def get_success_url(self):
        return reverse('myadmin:bespoke-orders-detail', args=[self.kwargs['pk']])

    def get_order(self):
        # Get the bespoke order object using the pk passed in the URL
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        # Get the context from the superclass, which includes the form for BespokeOrder
        context = super().get_context_data(**kwargs)

        # Initialize the staff formset based on the request method
        if self.request.POST:
            print(self.request.POST)

            context['staff_info_formset'] = BespokeOrderStaffInfoFormSet(
                self.request.POST, instance=self.object)
        else:
            context['staff_info_formset'] = BespokeOrderStaffInfoFormSet(
                instance=self.object)
        print(dir(context['staff_info_formset']))
        return context

    def form_invalid(self, form):
        # Handle invalid form submission and ensure the formset is also passed to the context
        context = self.get_context_data(form=form)

        # Display messages and re-render form with errors
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(context)

    def form_valid(self, form):
        # Ensure both the main form and the formset are valid before saving
        context = self.get_context_data()
        staff_info_formset = context['staff_info_formset']

        if form.is_valid() and staff_info_formset.is_valid():
            # Save the main form to update the BespokeOrder instance
            self.object = form.save()

            # Associate and save the staff info formset with the updated instance
            staff_info_formset.instance = self.object
            staff_info_formset.save()

            messages.success(
                self.request, f"Bespoke order for {self.object.client} and related staff info updated successfully!"
            )
            return redirect(self.get_success_url())
        else:
            # If form or formset is invalid, re-render with errors
            messages.error(self.request, "Please correct the errors below.")
            return self.form_invalid(form)


class BespokeOrderUpdateViewX(UpdateView):
    model = BespokeOrder
    form_class = BespokeOrderForm
    # Replace with your template name
    template_name = 'bespoke_orders/bespoke_order_form.html'
    # Redirect URL after successful save
    success_url = reverse_lazy('bespoke_order_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Inline formsets for BespokeOrderStaffInfo and BespokeOrderStatusLog
        if self.request.POST:
            context['staff_info_formset'] = inlineformset_factory(
                BespokeOrder, BespokeOrderStaffInfo,
                form=BespokeOrderStaffInfoForm, extra=1, can_delete=True
            )(self.request.POST, instance=self.object, prefix='staff')

            context['status_log_formset'] = inlineformset_factory(
                BespokeOrder, BespokeOrderStatusLog,
                form=BespokeOrderStatusLogForm, extra=1, can_delete=True
            )(self.request.POST, instance=self.object, prefix='status')
        else:
            context['staff_info_formset'] = inlineformset_factory(
                BespokeOrder, BespokeOrderStaffInfo,
                form=BespokeOrderStaffInfoForm, extra=1, can_delete=True
            )(instance=self.object, prefix='staff')

            context['status_log_formset'] = inlineformset_factory(
                BespokeOrder, BespokeOrderStatusLog,
                form=BespokeOrderStatusLogForm, extra=1, can_delete=True
            )(instance=self.object, prefix='status')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        staff_info_formset = context['staff_info_formset']
        status_log_formset = context['status_log_formset']

        # Check if both main form and formsets are valid
        if form.is_valid() and staff_info_formset.is_valid() and status_log_formset.is_valid():
            self.object = form.save()  # Save main form to get `BespokeOrder` instance
            # Associate formset instances with main form
            staff_info_formset.instance = self.object
            status_log_formset.instance = self.object
            staff_info_formset.save()  # Save formset data
            status_log_formset.save()
            messages.success(
                self.request, "Bespoke order and related staff info updated successfully!")
            return redirect(self.get_success_url())

        else:
            # If form or formsets are invalid, render the form with errors
            messages.error(self.request, "Please correct the errors below.")
            return self.form_invalid(form)


class ClientBespokeOrdersView(ListView):
    model = BespokeOrderStatusLog
    template_name = 'bespoke_orders/client_bespoke_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        # Get the client object
        client = get_object_or_404(Client, pk=self.kwargs['client_pk'])

        # Get the status parameter from the URL
        status = self.kwargs['status'].upper()

        # If the status is 'ALL', return all orders
        if status == 'ALL':
            return client.bespoke_order.all().distinct()

        # Filter the orders based on the given status, if it's a valid status
        if status in ['PENDING', 'DELIVERED', 'IN_PROGRESS', 'CANCELLED']:
            return client.bespoke_order.filter(
                status_log__status=status
            ).distinct()

        # Default: return all orders excluding delivered ones if status is invalid
        return client.bespoke_order.exclude(
            status_log__status=BespokeOrderStatusLog.DELIVERED
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the client object to the context
        client = get_object_or_404(Client, pk=self.kwargs['client_pk'])
        context['client'] = client
        context['new_orders_count'] = BespokeOrder.created_in_last_week(True)

        # Add available statuses for tab navigation
        context['available_statuses'] = ['ALL', 'PENDING',
                                         'IN PROGRESS', 'DELIVERED', 'CANCELLED']

        # Add the selected status
        context['selected_status'] = self.kwargs['status'].upper() or "ALL"

        return context
