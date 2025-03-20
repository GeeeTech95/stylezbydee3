from django.urls import path, include
from django.urls import path
from . import clients,staffs



urlpatterns = [
    #CLIENT
    path('clients/<int:pk>/update/', clients.ClientUpdateView.as_view(), name='client-update-api'),
    path('clients/<int:pk>/delete/', clients.ClientDeleteView.as_view(), name='client-delete-api'),


    #STAFF
    path('staffs/create-salary-log/', staffs.CreateSalaryLogView.as_view(), name='create-salary-log-api'),
    path('staffs/<int:pk>/delete/', staffs.StaffDeleteView.as_view(), name='staff-delete-api'),

 

]

 