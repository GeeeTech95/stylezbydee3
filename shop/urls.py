from django.urls import path
from . import product, explore, checkout

urlpatterns = [
    #PRODUCT
    path("item/<str:slug>/detail/",product.ProductDetail.as_view(), name="product-detail"),


    #EXPLORE 
    path("explore-collection/",explore.ExploreCollection.as_view(),name = 'explore-collection'),
    path("explore-shop/",explore.ExploreShop.as_view(),name = 'explore-shop'),

    #CART
    path("shopping-cart/",checkout.ShoppingCart.as_view(),name = "shopping-cart"),

    #CHECKOUT
    path("checkout/",checkout.SiteCheckout.as_view(),name = 'site-checkout'),
    path("checkout/chat/",checkout.ChatCheckout.as_view(),name = 'chat-checkout'),
    
]