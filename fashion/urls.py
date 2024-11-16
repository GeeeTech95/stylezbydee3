from django.urls import path
from . import tailoring

urlpatterns = [
    path("custom-tailoring/",tailoring.CustomTailoring.as_view(),name = 'custom-tailoring'),
    path("catalogue/",tailoring.Catalogue.as_view(),name = 'fashion-catalogue'),

    #
    path("custom-tailoring/how-it-works/",tailoring.HowItWorks.as_view(),name = "how-it-works")

]