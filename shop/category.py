from django import template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404
from django.urls.base import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse
from django.template.loader import render_to_string

from .models import ProductCategory



class CategoryDetail(generic.DetailView) :
    model = ProductCategory
    template_name = "explore-shop.html"
    context_object_name = "category"

    def get_context_data(self,**kwargs) :
        ctx = super(CategoryDetail,self).get_context_data(**kwargs)
        return ctx

