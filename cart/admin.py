from django.contrib import admin

from .models import *

admin.site.register(Cart)
admin.site.register(CartLine)
admin.site.register(CartLineAttribute)
