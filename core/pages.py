from typing import Any
from django.views import generic
from shop.models import Product


class HomePage(generic.TemplateView) :
    template_name = "index.html"

    def get_context_data(self, **kwargs: Any) :
        ctx = super(HomePage,self).get_context_data(**kwargs)
        ctx['new_arrivals'] = Product.objects.all().order_by("-created_at")[:6]
        ctx['best_selling'] = Product.objects.all()[:6]
        return ctx
    


class Contact(generic.TemplateView) :
    template_name = "contact.html"

    def get_context_data(self, **kwargs: Any) :
        ctx = super(Contact,self).get_context_data(**kwargs)
        return ctx



class Test(generic.TemplateView) :
    template_name = "checkout.html"
