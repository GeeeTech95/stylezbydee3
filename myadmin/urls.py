from django.urls import path
from . import views, clients, bespoke_orders, staff, catalogue


app_name = 'myadmin'  # This sets the app namespace


urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),

    # CATALOGUE
    path("catalogue/", catalogue.CatalogueListView.as_view(), name='catalogue-list'),
    path('catalogue/create/', catalogue.CatalogueCreateView.as_view(),
         name='catalogue-create'),  # Create view

    path('catalogue/<int:pk>/', catalogue.CatalogueDetailView.as_view(),
         name='catalogue-detail'),
    path('catalogue/<int:pk>/edit/',
         catalogue.CatalogueEditView.as_view(), name='edit-catalogue'),
    path('catalogue/<int:pk>/delete/',
         catalogue.CatalogueDeleteView.as_view(), name='delete-catalogue'),



    # CLIENTS
    path('clients/', clients.ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', clients.ClientDetailView.as_view(),
         name='client-detail'),
    path('clients/create/', clients.ClientCreateView.as_view(), name='client-create'),
    path('clients/<int:pk>/update/<str:target_form>/',
         clients.ClientUpdateView.as_view(), name='client-update'),




    # BESPOKE ORDERS
    path('bespoke-orders/<str:status>/',
         bespoke_orders.BespokeOrderListView.as_view(), name='bespoke-orders-list'),

    path('bespoke-orders/<int:pk>/detail/',
         bespoke_orders.BespokeOrderDetailView.as_view(), name='bespoke-orders-detail'),

    path('bespoke-orders/<int:pk>/update/',
         bespoke_orders.BespokeOrderUpdateView.as_view(), name='bespoke-orders-update'),

    path('bespoke-orders/<int:pk>/status/update/',

         bespoke_orders.BespokeOrderStatusUpdate.as_view(), name='bespoke-orders-status-update'),

    path('clients/<str:client_pk>/bespoke-orders/create/',
         bespoke_orders.BespokeOrderCreateView.as_view(), name='bespoke-orders-create'),

    path('client/<str:client_pk>/bespoke-orders/<str:status>/',
         bespoke_orders.ClientBespokeOrdersView.as_view(), name='client-bespoke-orders'),


    # STAFFS
    path('staffs/', staff.StaffListView.as_view(), name='staff-list'),
    path('staffs/add/', staff.StaffCreateView.as_view(), name='staff-create'),
    path('staffs/<int:pk>/', staff.StaffDetailView.as_view(), name='staff-detail'),
    path('staffs/<int:pk>/update/',
         staff.StaffUpdateView.as_view(), name='staff-update'),
    path('staffs/<int:pk>/delete/',
         staff.StaffDeleteView.as_view(), name='staff-delete'),


    path('staffs/salary-logs/', staff.SalaryLogListView.as_view(),
         name='salary-log-list'),
    path('staffs/salary-log/mark-paid/<int:pk>/',
         staff.MarkSalaryPaidView.as_view(), name='mark-salary-paid'),






    # STAFF transactions
    path('staffs/transactions/', staff.StaffTransactionLogListView.as_view(),
         name='transactions-log-list'),
    path('staffs/<int:staff_pk>/transactions/',
         staff.StaffTransactionLogListView.as_view(), name='staff-transactions-log-list'),

    # STAFF transactions
    path('staffs/transactions/<int:pk>/', staff.StaffTransactionLogListView.as_view(),
         name='transaction-log-detail'),
    path('staffs/transactions/add/', staff.StaffTransactionLogCreateView.as_view(),
         name='transactions-log-create'),
    path('staffs/transactions/<int:pk>/edit/',
         staff.StaffTransactionLogUpdateView.as_view(), name='transaction-log-update'),



]
