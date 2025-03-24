from django.urls import path, include
from django.contrib.auth import views as auth_views
from .staff import views as staff_views,bespoke_order,dashboard as staff_dashboard,profile
from . import accounts,dashboard,auth



urlpatterns = [

    #AUTH  
    path("register/",accounts.RegisterView.as_view(),name='register'),
    path("login/",accounts.LoginFormView.as_view(),name='login'),

    
    #DJANGO PASOWRD RESET CONTRIB
    path('password-reset/', auth.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password/password_reset_complete.html'), name='password_reset_complete'),


 


    #DASHBOARD
    path("dashboard/",dashboard.Dashboard.as_view(),name = 'dashboard'),

    
    #STAFF
    path("staff/dashboard/",staff_dashboard.Dashboard.as_view(),name = 'staff-dashboard'),
    path("staff/bespoke-orders/<str:status>/",bespoke_order.BespokeOrderListView.as_view(),name = 'staff-bespoke-orders'),
    path("staff/bespoke-orders/<int:pk>/detail/",bespoke_order.BespokeOrderDetailView.as_view(),name = 'staff-bespoke-order-detail'),
    path('staff/bespoke-orders/<int:pk>/staff-status/update/', staff_views.UpdateStaffBespokeOrderStatusView.as_view(), name='staff-update-bespoke-order-status'),

    path('staffs/profile/', profile.StaffProfileView.as_view(), name='staff-profile'),
    path('staffs/profile/update/', profile.StaffProfileUpdateView.as_view(), name='staff-profile-update'),

]
