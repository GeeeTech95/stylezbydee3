from typing import Any
from django.db import models
from django.views import generic
from .models import Order
from django.shortcuts import get_object_or_404



class OrderDetail(generic.DetailView):
    model = Order
    template_name = "order-detail.html"

    def get_object(self) :
        return get_object_or_404(self.model,number = self.kwargs['number'])
