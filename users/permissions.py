
class ActivityPermissions () :

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
