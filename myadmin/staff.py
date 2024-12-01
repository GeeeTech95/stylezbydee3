from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, View,UpdateView, DeleteView
from .models import Staff,StaffTransactionLog,StaffSalaryLog
from .forms import StaffForm, StaffTransactionLogForm,StaffSalaryLogForm
from django.contrib import messages
from django.http import HttpResponseForbidden
from .utils import Salary as SalaryUtils
from django.views.generic.detail import SingleObjectMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from users.permissions import ActivityPermissions
from django.contrib import messages
from django.shortcuts import get_object_or_404



class StaffListView(ListView):
    model = Staff
    template_name = 'staff/staff_list.html'
    context_object_name = 'staffs'

    def get_context_data(self, **kwargs) :
        ctx =  super(StaffListView,self).get_context_data(**kwargs)
        ctx['total_staff_count'] = self.model.objects.count()
        return ctx


class StaffCreateView(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('myadmin:staff-list')
    
    def form_valid(self, form):
        # Add a success message
        messages.success(self.request, "Staff member created successfully!")
        return super().form_valid(form)


class StaffDetailView(DetailView):
    model = Staff
    template_name = 'staff/staff_detail.html'
    context_object_name = 'staff'


class StaffUpdateView(UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('myadmin:staff-list')


class StaffDeleteView(DeleteView):
    model = Staff
    template_name = 'staff/staff_confirm_delete.html'
    success_url = reverse_lazy('staff-list')





class StaffTransactionLogListView(ListView):
    model = StaffTransactionLog
    template_name = 'staff/staff_transaction_list.html'
    context_object_name = 'transaction_logs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        staff_pk = self.kwargs.get('staff_pk')
        if staff_pk:
            # Filter transactions for the specified staff
            queryset = queryset.filter(staff_id=staff_pk)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_pk = self.kwargs.get('staff_pk')
        if staff_pk:
            staff = get_object_or_404(Staff, pk=staff_pk)
            context['staff'] = staff
            context['title'] = "All Transactions For {}".format(staff)
        else :
            context['title'] = "All Transactions"
        return context




# Create View for Transaction Log
class StaffTransactionLogCreateView(CreateView):
    model = StaffTransactionLog
    form_class = StaffTransactionLogForm
    template_name = 'staff/staff_transaction_log_form.html'
    success_url = reverse_lazy('myadmin:transactions-log-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        transaction_log = form.instance  # The saved instance of the StaffTransactionLog
        messages.success(self.request, '{} transaction log of ₦{:,.2f}  for {} has been successfully created.'.format(
            transaction_log.transaction_type.capitalize(),  # Example: 'Credit' or 'Debit'
            transaction_log.amount   ,
            transaction_log.staff,       
        ))
        return response


     



# Update View for Transaction Log
class StaffTransactionLogUpdateView(UpdateView):
    model = StaffTransactionLog
    form_class = StaffTransactionLogForm
    template_name = 'transaction_log_form.html'
    success_url = reverse_lazy('transaction_log_list')



# List View to show Salary Logs
class SalaryLogListView(ListView):
    model = StaffSalaryLog
    template_name = 'staff/staff_salary_log_list.html'
    context_object_name = 'salary_logs'

    def get_queryset(self):
        #run a function
        SalaryUtils.create_salary_logs()
        return []

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Salary Logs'
        context['paid_salaries'] = StaffSalaryLog.objects.filter(is_paid=True)
        context['unpaid_salaries'] = StaffSalaryLog.objects.filter(is_paid=False)
        return context




class MarkSalaryPaidView(LoginRequiredMixin,UserPassesTestMixin, SingleObjectMixin, View):
    model = StaffSalaryLog

    def test_func(self) :
        perm = ActivityPermissions(self.request.user)
        return perm.can_pay_salaries()
        
    

    def post(self, request, *args, **kwargs):
        salary_log = self.get_object()
        
        # Ensure it's an unpaid log before marking it as paid
        if not salary_log.date_paid:
            salary_log.date_paid = timezone.now()
            salary_log.amount_paid = salary_log.amount_due #for now
            salary_log.is_paid = True
            salary_log.save()

        # Provide feedback to the client-side, could be JSON or simple redirect
       
        return JsonResponse({'success': True, 'new_status': 'paid'})

    


