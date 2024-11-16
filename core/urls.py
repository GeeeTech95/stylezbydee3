from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import pages,views


urlpatterns = [
    path('', pages.HomePage.as_view(), name='home'),
    path('contact/', pages.Contact.as_view(), name='contact'),
    path('login-redirect/', views.my_redirect_view, name='login-redirect'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]


