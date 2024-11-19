
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.views.generic import TemplateView

from fashion.models import BespokeOrder,BespokeOrderStatusLog
from .models import StaffSalaryLog
from .utils import Charts

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure the user is an admin (superuser or staff)."""

    def test_func(self):
        # Check if the user is active and is a staff member (has access to the admin).
        return self.request.user.is_active and self.request.user.is_staff

    def handle_no_permission(self):
        # Redirect to the admin login page if the test fails
        return redirect(reverse('admin:login'))




class Dashboard(AdminRequiredMixin, TemplateView):
    template_name = "admin-dashboard.html"

    def get_context_data(self, **kwargs ) :
        ctx = super().get_context_data(**kwargs)
        ctx['bespoke_orders_count'] = BespokeOrder.objects.count()
        ctx['completed_bespoke_orders_count'] = BespokeOrder.get_completed_bespoke_orders(True)
        ctx['completed_bespoke_orders_percent'] = (ctx['completed_bespoke_orders_count'] / ctx['bespoke_orders_count']) * 100 if ctx['bespoke_orders_count'] else 0
        ctx['unpaid_salaries'] = StaffSalaryLog.objects.filter(is_paid=False)[:5]
        ctx.update(Charts.bespoke_order_chart_view())
        
        return ctx
