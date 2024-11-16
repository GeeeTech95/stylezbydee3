from typing import Any
from django.views import generic
from .models import Product



class ProductDetail(generic.DetailView) :
    template_name = "product-detail.html"
    model = Product 

    def get_context_data(self, **kwargs) :
        ctx = super(ProductDetail,self).get_context_data(**kwargs)
        ctx['currency'] = self.request.COOKIES.get('currency','USD')
        return ctx