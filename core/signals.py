from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.shortcuts import redirect

@receiver(user_logged_in)
def redirect_after_login(sender, request, user, **kwargs):
    if user.is_superuser:
        return redirect('myadmin:dashboard')