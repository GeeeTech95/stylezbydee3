from django.contrib import admin
from .models import BespokeOrder, Client, Catalogue, BespokeOrderStaffInfo, CatalogueImage, BespokeOrderStatusLog, Staff, ClientBodyMeasurement

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
    """Inline admin for managing catalogue images directly within the catalogue admin."""
    model = CatalogueImage
    fields = ('image', 'alt_text', 'position', 'created_at', 'updated_at')  # Fields to display
    readonly_fields = ('created_at', 'updated_at')  # Non-editable fields
    extra = 1  # Number of empty forms to display for new images
    ordering = ['position']  # Order images by position


@admin.register(Catalogue)
class CatalogueAdmin(admin.ModelAdmin):
    """Admin configuration for the Catalogue model."""
    list_display = (
        'title', 
        'category', 
        'cost', 
        'discount_price', 
        'get_final_price', 
        'is_discounted', 
        'created_at', 
        'updated_at'
    )  # Columns to display in the admin list view
    list_filter = ('category', 'created_at', 'updated_at')  # Filters for quick navigation
    search_fields = ('title', 'description_text')  # Enables search functionality
    prepopulated_fields = {'slug': ('title',)}  # Automatically populates slug from title
    readonly_fields = ('created_at', 'updated_at')  # Prevents editing timestamps
    inlines = [CatalogueImageInline]  # Includes images as inline fields
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'slug', 'description_text', 'category')
        }),
        ('Pricing', {
            'fields': ('cost', 'discount_price')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def get_final_price(self, obj):
        """Display the calculated final price in the admin."""
        return obj.get_final_price()

    get_final_price.short_description = 'Final Price'
    get_final_price.admin_order_field = 'cost'  # Allows sorting by cost


@admin.register(CatalogueImage)
class CatalogueImageAdmin(admin.ModelAdmin):
    """Admin configuration for standalone management of Catalogue Images."""
    list_display = ('catalogue', 'alt_text', 'position', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'catalogue')
    search_fields = ('alt_text', 'catalogue__title')
    ordering = ['catalogue', 'position']  # Orders by catalogue and position



admin.site.register(ClientBodyMeasurement)
