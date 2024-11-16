from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class UserAdmin(BaseUserAdmin):
    # Fields that will be shown when creating a user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'password1', 'password2'),
        }),
    )

    # Fields that will be shown when editing a user
    fieldsets = (
        (None, {'fields': ('account_id','email', 'password')}),
        (_('Personal info'), {'fields': ('full_name', 'phone_number', 'gender', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # List of fields that are displayed in the admin user list
    list_display = ('email', 'full_name', 'is_staff', 'is_active', 'user_type')
    
    # Fields that will be searchable in the admin list
    search_fields = ('email', 'full_name')
    
    # Fields to be read-only when editing a user
    readonly_fields = ('account_id', 'email_verified', 'phone_number_verified', 'date_joined', 'last_login')

    ordering = ('email',)

# Register the user model and custom admin
admin.site.register(User, UserAdmin)



admin.site.register(Security)
admin.site.register(NotificationCategory)
admin.site.register(Notification)
