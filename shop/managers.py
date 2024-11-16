from django.db import models
from django.db.models import Count, Sum, F, Q
from django.db.models.manager import BaseManager
from django.utils import timezone



class ItemQuerySet(models.query.QuerySet) :
    
    def top_items(self,user=None, campus=None):
        queryset = self
        if campus:
            queryset = queryset.filter(campus=campus)
        return queryset







class ProductManager(BaseManager.from_queryset(ItemQuerySet)) :

    def get_queryset(self):
        queryset = super(ProductManager, self).get_queryset()
        return queryset
    

    def recommend_products(self,user,campus = None) :
        queryset = self.get_queryset()
        return queryset

    def trending(self,user=None) :
        queryset = self.get_queryset()
        print(queryset)
        return queryset     

    
    def latest(self,user=None,campus = None) :
        queryset = self.get_queryset()
        queryset = queryset.order_by("-created_at")
        return queryset     

    def today_deals(self,user=None,campus=None)  :
        queryset = self.get_queryset()
        if campus :
            queryset = queryset.filter(campus = campus)
        """ price change must have occured in the past
        7 days"""
        time_limit = timezone.now() - timezone.timedelta(days = 7)
   
        queryset = queryset.filter(
            price__lt = F("old_price"),
            last_modified__gte = time_limit
            ).annotate(
                percentage_discount  = (F("old_price") - F("price"))/F("old_price")
            ).order_by("-percentage_discount") 
        
        return queryset
