from django.shortcuts import render,redirect
from django.urls import reverse

# Create your views here.
def error_404_handler(request,exception) :
    template_name = "404.html"
    return render(request,template_name,locals())


def error_500_handler(request) :
    template_name = "500.html"
    return render(request,template_name,locals())

def error_403_handler(request,exception) :
    template_name = "403.html"
    return render(request,template_name,locals())



def my_redirect_view(request):
    # Redirect to a different URL
    if request.user.is_authenticated and request.user.is_staff :
        return redirect(reverse("myadmin:dashboard"))
    else :
        return redirect(reverse("home")) 



