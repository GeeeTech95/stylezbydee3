from django.urls import path
from . import views



urlpatterns = [

   path("shipment/detail/<str:tracking_number>/",views.ShipmentDetail.as_view(),name="shipment-detail"),
   path("shipment/track-shipment/",views.TrackShipment.as_view(),name="track-shipment")

]