from django.urls import path
from . import order


urlpatterns = [
    path("<int:number>/", order.OrderDetail.as_view(), name='order-detail')
]
