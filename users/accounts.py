from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views.generic import CreateView, View, RedirectView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .models import  User
from .forms import UserForm,LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect




class LoginFormView(FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = '/'  # Redirect to the home page upon successful login

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid login credentials")
            return self.form_invalid(form)




class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = UserForm
    success_url = reverse_lazy("login")  # Redirect to the login page upon successful registration


    def form_valid(self, form):
        form.save()
        return super().form_valid(form)




class LoginRedirect(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_admin:
            return HttpResponseRedirect((reverse('admin-dashboard')))
        else:
            return HttpResponseRedirect((reverse('dashboard')))


