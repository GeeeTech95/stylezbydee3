from django.urls import path 
from . import product,search


urlpatterns = [
      path("items/l/",product.ProductList.as_view(),name="product-list-api"),
      path("items/update-filters/",search.UpdateFilters.as_view(),name='update-filters-api'),

]