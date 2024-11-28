from django import template

register = template.Library()



@register.filter
def has_custom_permission(user, permission_name):
    if not user.is_authenticated:
        return False
    if hasattr(user, "custom_permissions"):
       
        return user.custom_permissions.filter(name=permission_name).exists()
    return False
