from django.urls import path,include
from . import order, checkout

urlpatterns  = [
   
    #CHECKOUT
    path("checkout/",checkout.Checkout.as_view(),name="checkout-api"),
]