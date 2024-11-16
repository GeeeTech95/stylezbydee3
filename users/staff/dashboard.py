from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.views.generic import TemplateView

from myadmin.models import Staff


class SiteAccess() :
   pass



class StaffRequiredMixin(UserPassesTestMixin):
    """Mixin to ensure the user is an admin (superuser or staff)."""

    def test_func(self):
        # Check if the user is active and is a staff member (has access to the admin).
        try :
            user = self.request.user
            return user.is_active and user.staff
        except Staff.DoesNotExist :
            return False
    
    def handle_no_permission(self):
        # Redirect to the admin login page if the test fails
        return redirect(reverse('login'))




class Dashboard(StaffRequiredMixin, TemplateView):
    template_name = "staff-dashboard.html"

    def get_context_data(self, **kwargs) :
        return super(Dashboard,self).get_context_data(**kwargs)


