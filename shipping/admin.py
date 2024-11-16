from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(Station)
admin.site.register(Shipment)
admin.site.register(StatusLog)
admin.site.register(TransitLog)


