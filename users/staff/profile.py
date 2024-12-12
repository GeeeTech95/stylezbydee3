from django.shortcuts import get_object_or_404
from myadmin.models import Staff
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from users.forms import UserUpdateForm

from django.urls import reverse_lazy
from django.contrib import messages


class StaffProfileView( LoginRequiredMixin,DetailView):
    model = Staff
    template_name = 'staff/staff-profile.html'
    context_object_name = 'staff'

    def get_object(self):
        return get_object_or_404(self.model,user = self.request.user)


class StaffProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'staff/staff_form.html'
    success_url = reverse_lazy('staff-profile')
   
    def get_object(self) :
        return self.request.user
        
    def form_valid(self, form):
        # Add a success message
        messages.success(self.request, "Profile Updated successfully!")
        return super().form_valid(form)
