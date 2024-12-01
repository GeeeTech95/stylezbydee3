from .models import CustomPermission



class ActivityPermissions () :
    model = CustomPermission

    def __init__(self,user) :
        self.user = user

    def can_approve_job_delegation(self) :
        if not self.user.is_staff :
            return False
        return True
    
    def can_pay_salaries(self) :
        if not self.user.is_staff :
            return False
        return True
    
    def has_custom_permission(self,permission_name):

        if not self.user.is_authenticated:
            return False
        if hasattr(self.user, "custom_permissions"):
        
            return self.user.custom_permissions.filter(name=permission_name).exists()
        return False
    
    
