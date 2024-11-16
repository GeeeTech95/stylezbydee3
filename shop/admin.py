from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import *


class CategoryAdmin(TreeAdmin):
    list_display = ('name', 'path')
    form = movenodeform_factory(ProductCategory)


class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('name',)

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'discount_type', 'discount_value')
    list_filter = ('start_date', 'end_date', 'discount_type')
    search_fields = ('name',)


admin.site.register(ProductCategory, CategoryAdmin)
admin.site.register(Product)
admin.site.register(ProductReview)
admin.site.register(ProductRecommendation)
admin.site.register(ProductMedia)
admin.site.register(ProductClass)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductAttributeOption)
admin.site.register(ProductAttributeOptionGroup)
admin.site.register(ProductCollection, CollectionAdmin)
admin.site.register(ProductSalePromotion, PromotionAdmin)

