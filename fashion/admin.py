from django.contrib import admin
from .models import BespokeOrder, Client, Catalogue, BespokeOrderStaffInfo, CatalogueImage, BespokeOrderStatusLog, Staff

class BespokeOrderStaffInfoInline(admin.TabularInline):
    model = BespokeOrderStaffInfo
    extra = 1
    fields = ('staff', 'delegation', 'pay', 'status', 'date_accepted', 'date_completed', 'date_approved')
    raw_id_fields = ('staff',)


class BespokeOrderStatusLogInline(admin.TabularInline):
    model = BespokeOrderStatusLog
    extra = 1
    fields = ('status', 'date')
    ordering = ['-date']  # Order by most recent status first


@admin.register(BespokeOrder)
class BespokeOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'client', 'style', 'total_cost', 'advance_payment')
    inlines = [BespokeOrderStaffInfoInline, BespokeOrderStatusLogInline]  # Add StatusLog inline here
    search_fields = ['client__name', 'style__name']
    list_filter = ['style']
    ordering = ['-id']  # Order by most recent first


@admin.register(BespokeOrderStatusLog)
class BespokeOrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ('outfit', 'status', 'date')
    search_fields = ['outfit__order_id', 'outfit__client__name', 'status']
    list_filter = ['status']
    ordering = ['-date']


@admin.register(BespokeOrderStaffInfo)
class BespokeOrderStaffInfoAdmin(admin.ModelAdmin):
    list_display = ('order', 'staff', 'delegation', 'pay', 'status', 'date_accepted', 'date_completed', 'date_approved')
    search_fields = ['order__client__name', 'staff__username']
    list_filter = ['delegation', 'status']
    ordering = ['-date_accepted']


class CatalogueImageInline(admin.TabularInline):
    model = CatalogueImage
    extra = 1


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', 'created_at', 'updated_at')
    search_fields = ['title', 'description_text']
    ordering = ['title']
    inlines = [CatalogueImageInline]


@admin.register(CatalogueImage)
class CatalogueImageAdmin(admin.ModelAdmin):
    list_display = ('catalogue', 'image', 'alt_text')
    search_fields = ['catalogue__title', 'alt_text']
    list_filter = ('catalogue',)
