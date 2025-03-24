from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import render

from .forms import CustomPasswordResetForm

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/password/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    html_email_template_name = 'registration/password_reset_email.html'

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        UserModel = get_user_model()

        if not UserModel.objects.filter(email__iexact=email, is_active=True).exists():
            context = {
                "title": "Password Reset Error",
                "message": "No account found with this email.",
                "back_link": reverse_lazy('password_reset'),
                "back_link_text": "Try Again",
            }
            return render(self.request, "generic-http-response.html", context, status=400)

        return super().form_valid(form)
