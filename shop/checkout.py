from django.views import generic
from django.http import HttpResponseRedirect
from  django.conf import settings


class ShoppingCart(generic.TemplateView) :
    template_name = "cart.html"



class SiteCheckout(generic.TemplateView) : 
    template_name = "checkout.html"


class ChatCheckout(generic.View) : 
    

    def get(self,request,*args,**kwargs) :
        #redirect to the appropriate social , eg whatsapp.
        url = "wa.me/{}".format(settings.SITE_WHATSAPP_NO)
        return HttpResponseRedirect(url)

