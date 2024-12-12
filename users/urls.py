from django.urls import path, include

from .staff import views as staff_views,bespoke_order,dashboard as staff_dashboard,profile
from . import accounts,dashboard



urlpatterns = [

    #AUTH  
    path("register/",accounts.RegisterView.as_view(),name='register'),
    path("login/",accounts.LoginFormView.as_view(),name='login'),
 


    #DASHBOARD
    path("dashboard/",dashboard.Dashboard.as_view(),name = 'dashboard'),

    
    #STAFF
    path("staff/dashboard/",staff_dashboard.Dashboard.as_view(),name = 'staff-dashboard'),
    path("staff/bespoke-orders/<str:status>/",bespoke_order.BespokeOrderListView.as_view(),name = 'staff-bespoke-orders'),
    path('staff/bespoke-orders/<int:pk>/staff-status/update/', staff_views.UpdateStaffBespokeOrderStatusView.as_view(), name='staff-update-bespoke-order-status'),

    path('staffs/profile/', profile.StaffProfileView.as_view(), name='staff-profile'),
    path('staffs/profile/update/', profile.StaffProfileUpdateView.as_view(), name='staff-profile-update'),

]
