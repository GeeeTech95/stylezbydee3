from django.urls import path, include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin-coded-target/', admin.site.urls),
    path("", include("core.urls")),
    path("shop/", include("shop.urls")),
    path("fashion/", include("fashion.urls")),
    path("order/", include("order.urls")),
    path("myadmin/", include("myadmin.urls", namespace='myadmin')),
    path("account/",include("users.urls")),
    # API
    path("api/v1/", include("core.api.v1.urls")),
    path("api/v1/", include("users.api.v1.urls")),
    path("api/v1/", include("fashion.api.v1.urls")),
    path("api/v1/shop/", include("shop.api.v1.urls")),
    path("api/v1/order/", include("order.api.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

else:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


handler404 = 'core.views.error_404_handler'
handler500 = 'core.views.error_500_handler'
handler403 = 'core.views.error_403_handler'
